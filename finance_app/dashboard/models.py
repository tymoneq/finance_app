from django.db import models
from django.contrib.auth.models import User

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
