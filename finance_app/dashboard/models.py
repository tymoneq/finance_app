from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Budget(models.Model):
    user_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="budgets"
    )
    budget_name = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.budget_name


class Category(models.Model):

    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name="allocations"
    )
    category_name = models.CharField(max_length=100, unique=False)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.category_name} : {self.percentage}"

class Loans(models.Model):
    user_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="loans"
    )
    loan_name = models.CharField(max_length=100, unique=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0.00), MaxValueValidator(1000000.00)])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[
        MinValueValidator(0.00), MaxValueValidator(100.00)])
    due_date = models.DateField()

    def __str__(self):
        return self.loan_name

class Investment(models.Model):
    user_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="investments"
    )
    investment_name = models.CharField(max_length=100, unique=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0.00), MaxValueValidator(1000000.00)])

    def __str__(self):
        return self.investment_name
    
class InvestmentCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    investments = models.ManyToManyField(Investment, related_name="categories")
