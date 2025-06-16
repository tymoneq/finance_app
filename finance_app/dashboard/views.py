from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .forms import BudgetForm, AllocationFormSet


# Create your views here.


class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"


class BudgetView(View):

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

        
        if formset.is_valid() and budget_form.is_valid():
            percentage_sum = 0

            for form in formset:
                percentage = form.cleaned_data.get("percentage")
                if percentage:
                    percentage_sum += percentage

            # dodaj kategorie others gdy procenty nie sumują się do 100%

            print(f"Total percentage: {percentage_sum}")
            if percentage_sum != 100:
                budget_form.add_error(None, "The total percentage must equal 100%")
                return render(
                    request,
                    "dashboard/budget.html",
                    {"budget": budget_form, "formset": formset},
                )

                # Process the valid forms
            return HttpResponseRedirect("/success/")

        return render(
            request,
            "dashboard/budget.html",
            {"budget": budget_form, "formset": formset},
        )


class CreditView(TemplateView):
    pass


class InvestmentsView(TemplateView):
    pass


class PortfolioView(TemplateView):
    pass


class NetWorthView(TemplateView):
    pass
