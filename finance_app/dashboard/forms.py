from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Loans

CATEGORY_CHOICES = [
    ("education", "Education"),
    ("savings", "Savings"),
    ("long-term-investing", "Long Term Investing"),
    ("offensive-investing", "Offensive Investing"),
    ("cost-of-living", "Cost of Living"),
    ("help-others", "Help Others"),
    ("dreams-and-whims", "Dreams and Whims"),
    ("food", "Food"),
    ("transport", "Transport"),
    ("entertainment", "Entertainment"),
    ("health", "Health"),
    ("other", "Other"),
    ("debt-repayment", "Debt Repayment"),
    ("vacation", "Vacation"),
    ("home-improvement", "Home Improvement"),
    ("miscellaneous", "Miscellaneous"),
    ("insurance", "Insurance"),
    ("taxes", "Taxes"),
    ("gifts", "Gifts"),
    ("subscriptions", "Subscriptions"),
    ("pets", "Pets"),
    ("travel", "Travel"),
]


class BudgetForm(forms.Form):
    budget_name = forms.CharField(max_length=100, label="Budget Name")
    money_amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")


class AllocationForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="Category")
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
