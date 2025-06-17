from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .forms import BudgetForm, AllocationForm
from .functions.pieChart import create_pie_chart
from django.forms import formset_factory

# Create your views here.
AllocationFormSet = formset_factory(
    AllocationForm, extra=3, can_delete=True, max_num=20, min_num=1
)


class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"


class BudgetView(View):
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
            "dashboard/budget.html",
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
            # creating pie chart
            context = create_pie_chart(budget_form, formset, context)
            return render(request, "dashboard/budget.html", context)

        return render(request, "dashboard/budget.html", context)


class CreditView(TemplateView):
    pass


class InvestmentsView(TemplateView):
    pass


class PortfolioView(TemplateView):
    pass


class NetWorthView(TemplateView):
    pass
