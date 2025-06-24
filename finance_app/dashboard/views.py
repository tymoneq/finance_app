from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.forms import formset_factory, modelformset_factory
from datetime import date

# My functions and models
from .models import (
    Budget,
    Category,
    Loans,
    Investment,
    InvestmentsThroughTime,
    NetWorth,
)
from .forms import (
    BudgetForm,
    AllocationForm,
    LoanForm,
    InvestmentForm,
)
from .functions.pieChart import (
    create_pie_chart_from_form,
    create_pie_chart_from_budget,
    create_a_pie_chart_from_investments,
)
from .functions.line_chart import create_line_chart
from .functions.calculating_total_amount import calculate_total_loan_amount

# Create your views here.
AllocationFormSet = formset_factory(
    AllocationForm, extra=3, can_delete=True, max_num=20, min_num=1
)
InvestmentFormSet = formset_factory(
    InvestmentForm, extra=3, can_delete=True, max_num=20, min_num=1
)


# All views in this file are related to the dashboard functionality of the application.


class DashboardView(TemplateView):
    """View for the dashboard.
    This view serves as the main entry point for the dashboard, providing an overview of the user's
    financial data, including budgets, loans, and investments.
    It renders the dashboard template and can be extended to include additional functionality in the future.
    """

    template_name = "dashboard/dashboard.html"


class BudgetView(LoginRequiredMixin, View):
    """View for managing the budget.
    This view handles both displaying the budget form and processing the submitted data.
    It includes a form for the budget and a formset for budget allocations.
    The budget form allows users to set a budget name and amount, while the allocation formset
    allows users to allocate percentages to various categories.
    """

    def get(self, request, *args, **kwargs):
        budget_form = BudgetForm(prefix="budget")
        allocation_formset = AllocationFormSet(prefix="allocations")
        return render(
            request,
            "dashboard/budget_creation.html",
            {"budget": budget_form, "formset": allocation_formset},
        )

    def post(self, request, *args, **kwargs):
        budget_form = BudgetForm(request.POST, prefix="budget")
        formset = AllocationFormSet(request.POST, prefix="allocations")

        context = {
            "budget": budget_form,
            "formset": formset,
        }

        if formset.is_valid() and budget_form.is_valid():

            action = request.POST.get("action")

            # creating pie chart
            if action == "submit_budget":
                context = create_pie_chart_from_form(budget_form, formset, context)

            if action == "save_budget":
                # Save the budget and allocations
                budget_name = budget_form.cleaned_data.get("budget_name")
                money_amount = budget_form.cleaned_data.get("money_amount")
                user = request.user
                # Check if a budget with the same name already exists for the user
                if Budget.objects.filter(user_name=user, budget_name=budget_name).exists():
                    context["message"] = "A budget with this name already exists."
                    return render(
                        request, "dashboard/budget_creation.html", context
                    )
                else:
                    budget = Budget.objects.create(
                        user_name=user, budget_name=budget_name, amount=money_amount
                    )
                    budget.save()

                for form in formset:

                    category_name = form.cleaned_data.get("category")
                    percentage = form.cleaned_data.get("percentage")

                    if category_name and percentage:
                        category = Category.objects.create(
                            category_name=category_name,
                            percentage=percentage,
                            budget=budget,
                        )
                        category.save()

                context["message"] = "Budget and allocations saved successfully."
                context = create_pie_chart_from_form(budget_form, formset, context)
                context["budget"] = BudgetForm(prefix="budget")  # Reset the budget form
                context["formset"] = AllocationFormSet(
                    prefix="allocations"
                )  # Reset the

        return render(request, "dashboard/budget_creation.html", context)


class BudgetListView(LoginRequiredMixin, ListView):
    """View for listing all budgets associated with the logged-in user.
    This view retrieves all budgets created by the user and displays them in a list format.
    It uses the ListView generic view to handle the retrieval and rendering of the budget data.
    """

    template_name = "dashboard/user_budgets.html"
    model = Budget
    context_object_name = "budgets"

    def get_queryset(self):
        return Budget.objects.filter(user_name=self.request.user).prefetch_related(
            "allocations"
        )


class BudgetDetailView(LoginRequiredMixin, TemplateView):
    """View for displaying the details of a specific budget.
    This view retrieves a budget by its primary key (pk) and displays its details,
    including the budget amount and its associated allocations.
    It also creates a pie chart from the budget allocations to visualize the distribution of the budget.
    """
    
    
    template_name = "dashboard/budget_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budget_id = self.kwargs.get("pk")
        budget = Budget.objects.prefetch_related("allocations").get(id=budget_id)
        context["budget"] = budget
        context["allocations"] = budget.allocations.all()
        # Create pie chart from budget allocations
        context = create_pie_chart_from_budget(context, budget.amount)
        return context


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a budget."""
    
    model = Budget
    success_url = reverse_lazy("your_budget")


class LoanView(LoginRequiredMixin, View):
    """View for managing loan-related information.
    This view handles displaying loan information and processing any related actions."""

    def get(self, request, *args, **kwargs):
        context = {
            "loan_form": LoanForm(prefix="loan"),
        }
        # Fetching loans related to the user
        user_loans = request.user.loans.all()
        if user_loans.exists():
            context["loans"] = user_loans
            context["total_amount"] = calculate_total_loan_amount(request.user)
        else:
            context["message"] = "No loans found for this user."

        return render(request, "dashboard/loan_view.html", context)

    def post(self, request, *args, **kwargs):
        loan_form = LoanForm(request.POST, prefix="loan")
        context = {"loan_form": loan_form}

        if loan_form.is_valid():
            loan = loan_form.save(commit=False)
            loan.user_name = request.user  # Associate the loan with the logged-in user
            loan.save()
            context["message"] = "Loan created successfully."
            user_loans = request.user.loans.all()
            context["loans"] = user_loans
            context["loan_form"] = LoanForm(
                prefix="loan"
            )  # Reset the form for new entry

        context["total_amount"] = calculate_total_loan_amount(request.user)

        return render(request, "dashboard/loan_view.html", context)


class LoanDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a loan."""
    model = Loans
    success_url = reverse_lazy("loans")


class PortfolioCreationView(LoginRequiredMixin, View):
    """View for managing the user's investment portfolio.
    This view handles displaying the portfolio and processing any related actions.
    It includes a form for adding investments and a form for managing investment categories.
    """

    def create_chart_data(self, request, context):
        """Helper function to create chart data for investments."""
        qs = InvestmentsThroughTime.objects.filter(user_name=request.user).all()
        context = create_line_chart(
            context,
            qs,
            ["date", "amount"],
            "Investments Over Time",
            y_axis_label="Investment Value",
        )
        return context

    def get(self, request, *args, **kwargs):
        investment_form = InvestmentFormSet()
        context = {
            "investment_form": investment_form,
        }
        context = self.create_chart_data(request, context)
        return render(request, "dashboard/portfolio_creation.html", context)

    def post(self, request, *args, **kwargs):
        investment_form = InvestmentFormSet(request.POST)
        context = {
            "investment_form": investment_form,
        }

        if investment_form.is_valid():
            action = request.POST.get("action")
            total_sum_of_investments = 0

            for form in investment_form:
                if form.cleaned_data.get("investment_name"):
                    investment = form.save(commit=False)
                    investment.user_name = request.user
                    investment.save()
                    total_sum_of_investments += form.cleaned_data.get("amount", 0)

            context["message"] = "Investments submitted successfully."

            # rendering a pie chart

            context = create_a_pie_chart_from_investments(
                investment_form, context, total_sum_of_investments
            )

            if action == "save_portfolio_value":
                current_date = date.today()
                exists = InvestmentsThroughTime.objects.filter(
                    user_name=request.user, date=current_date
                ).exists()

                if not exists:
                    InvestmentsThroughTime.objects.create(
                        user_name=request.user,
                        amount=total_sum_of_investments,
                        date=current_date,
                    )

                if exists:
                    InvestmentsThroughTime.objects.filter(
                        user_name=request.user, date=current_date
                    ).update(amount=total_sum_of_investments)

            context = self.create_chart_data(request, context)

            context["investment_form"] = (
                InvestmentFormSet()
            )  # Reset the formset for new entry

        return render(request, "dashboard/portfolio_creation.html", context)


class NetWorthView(LoginRequiredMixin, TemplateView):
    """View for displaying the user's net worth.
    This view calculates the user's net worth based on their investments and loans,
    and displays it over time using a line chart.
    It updates the net worth daily and provides a historical view of the user's financial health.
    """
    
    template_name = "dashboard/net_worth.html"

    def update_net_worth(self, request):
        current_date = date.today()
        exists = NetWorth.objects.filter(
            user_name=request.user, date=current_date
        ).exists()

        # Calculate total net worth
        total_net_worth = 0.00
        total_net_worth -= float(calculate_total_loan_amount(request.user))
        last_investments = InvestmentsThroughTime.objects.filter(
            user_name=request.user
        ).last()
        last_investments_amount = last_investments.amount if last_investments else 0.00
        total_net_worth += float(last_investments_amount)

        if not exists:
            NetWorth.objects.create(
                user_name=request.user,
                total_net_worth=total_net_worth,
                date=current_date,
            )

        if exists:
            NetWorth.objects.filter(user_name=request.user, date=current_date).update(
                total_net_worth=total_net_worth
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.update_net_worth(self.request)
        user = self.request.user
        qs = NetWorth.objects.filter(user_name=user).all()

        context = create_line_chart(
            context,
            qs,
            ["date", "total_net_worth"],
            "Net Worth Over Time",
            y_axis_label="Net Worth Value",
        )

        return context
