from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator 

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
        max_digits=5, decimal_places=2, label="Percentage of Income", validators=[
            MinValueValidator(0.01),
            MaxValueValidator(100.00)
        ]
    )



