from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.forms import formset_factory, modelformset_factory
from datetime import date

# My functions and models
from .models import Budget, Category, Loans, Investment, InvestmentsThroughTime
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
from .functions.line_chart import create_line_chart_from_investments
from .functions.calculating_total_amount import calculate_total_loan_amount

# Create your views here.
AllocationFormSet = formset_factory(
    AllocationForm, extra=3, can_delete=True, max_num=20, min_num=1
)
InvestmentFormSet = formset_factory(
    InvestmentForm, extra=3, can_delete=True, max_num=20, min_num=1
)


class DashboardView(TemplateView):
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
    template_name = "dashboard/user_budgets.html"
    model = Budget
    context_object_name = "budgets"

    def get_queryset(self):
        return Budget.objects.filter(user_name=self.request.user).prefetch_related(
            "allocations"
        )


class BudgetDetailView(LoginRequiredMixin, TemplateView):
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
    model = Loans
    success_url = reverse_lazy("loans")


class PortfolioCreationView(LoginRequiredMixin, View):
    """View for managing the user's investment portfolio.
    This view handles displaying the portfolio and processing any related actions.
    It includes a form for adding investments and a form for managing investment categories.
    """

    def get(self, request, *args, **kwargs):
        investment_form = InvestmentFormSet()
        context = {
            "investment_form": investment_form,
        }

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

                qs = InvestmentsThroughTime.objects.filter(user_name=request.user).all()

                data = list(qs.values_list("date", "amount"))
                investments_data = {
                    "x": [d[0] for d in data],
                    "y": [d[1] for d in data],
                }
                context = create_line_chart_from_investments(
                    investments_data, context, "Investments Over Time", 'Date', 'Investment Value'
                )

            context["investment_form"] = (
                InvestmentFormSet()
            )  # Reset the formset for new entry

        return render(request, "dashboard/portfolio_creation.html", context)


class NetWorthView(TemplateView):
    pass
