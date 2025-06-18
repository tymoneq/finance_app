from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView
from django.http import HttpResponseRedirect
from .forms import BudgetForm, AllocationForm, LoanForm
from django.urls import reverse_lazy
from .functions.pieChart import create_pie_chart_from_form, create_pie_chart_from_budget
from .functions.loans_total_amount import calculate_total_loan_amount
from django.forms import formset_factory
from .models import Budget, Category, Loans
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
AllocationFormSet = formset_factory(
    AllocationForm, extra=3, can_delete=True, max_num=20, min_num=1
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
                context["formset"] = AllocationFormSet(prefix="allocations")  # Reset the

            return render(request, "dashboard/budget_creation.html", context)

        return render(request, "dashboard/budget_creation.html", context)


class BudgetListView(LoginRequiredMixin, ListView):
    template_name = "dashboard/user_budgets.html"
    model = Budget
    context_object_name = "budgets"

    def get_queryset(self):
        return Budget.objects.prefetch_related("allocations")


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


class PortfolioView(TemplateView):
    pass


class NetWorthView(TemplateView):
    pass
