from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from .forms import BudgetForm, AllocationForm
from .functions.pieChart import create_pie_chart
from django.forms import formset_factory
from .models import Budget, Category
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
                context = create_pie_chart(budget_form, formset, context)
                
            if action == "save_budget":
                # Save the budget and allocations
                budget_name = budget_form.cleaned_data.get("budget_name")
                money_amount = budget_form.cleaned_data.get("money_amount")
                user = request.user
                
                budget = Budget.objects.create(user_name=user, budget_name=budget_name, amount=money_amount)
                budget.save()
                
                for form in formset:

                    category_name = form.cleaned_data.get("category")
                    percentage = form.cleaned_data.get("percentage")
                    
                    if category_name and percentage:
                        category = Category.objects.create(category_name=category_name, percentage=percentage, budget=budget)
                        category.save()
                
                context["message"] = "Budget and allocations saved successfully."
                context = create_pie_chart(budget_form, formset, context)

            return render(request, "dashboard/budget_creation.html", context)

        return render(request, "dashboard/budget_creation.html", context)


class BudgetListView(LoginRequiredMixin, ListView):
    template_name = "dashboard/user_budgets.html"
    model = Budget
    context_object_name = "budgets"
    
    def get_queryset(self):
        return Budget.objects.prefetch_related("allocations")


class CreditView(TemplateView):
    pass


class InvestmentsView(TemplateView):
    pass


class PortfolioView(TemplateView):
    pass


class NetWorthView(TemplateView):
    pass
