from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Loans, Investment
from .list_and_dictionaries.statuses import (
    BUDGET_CATEGORY_CHOICES,
    INVESTMENT_CATEGORIES,
)


class BudgetForm(forms.Form):
    budget_name = forms.CharField(max_length=100, label="Budget Name")
    money_amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")


class AllocationForm(forms.Form):
    category = forms.ChoiceField(choices=BUDGET_CATEGORY_CHOICES, label="Category")
    percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Percentage of Income",
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)],
    )


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loans
        fields = ["loan_name", "amount", "interest_rate", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "loan_name": "Loan Name",
            "amount": "Loan Amount",
            "interest_rate": "Interest Rate (%)",
            "due_date": "Due Date",
        }
        help_texts = {
            "amount": "Enter the total amount of the loan.",
            "interest_rate": "Enter the annual interest rate in percentage.",
            "due_date": "Select the due date for the loan repayment.",
        }
        error_messages = {
            "loan_name": {
                "max_length": "This loan name is too long.",
                "required": "Please enter a loan name.",
            },
            "amount": {
                "required": "Please enter the loan amount.",
                "invalid": "Enter a valid amount.",
            },
            "interest_rate": {
                "required": "Please enter the interest rate.",
                "invalid": "Enter a valid interest rate.",
            },
            "due_date": {
                "required": "Please select a due date.",
            },
        }


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ["investment_name", "amount", "category_name"]
        labels = {
            "investment_name": "Investment Name",
            "amount": "Investment Amount",
            "category_name": "Investment Category",
        }
        help_texts = {
            "amount": "Enter the total amount of the investment.",
        }
        error_messages = {
            "investment_name": {
                "max_length": "This investment name is too long.",
                "required": "Please enter an investment name.",
            },
            "amount": {
                "required": "Please enter the investment amount.",
                "invalid": "Enter a valid amount.",
            },
        }


