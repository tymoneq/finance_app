from django.contrib import admin
from .models import Budget, Category, Loans, Investment, InvestmentsThroughTime, NetWorth

# Register your models here.


class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user_name", "budget_name", "amount")
    search_fields = ("budget_name",)
    list_filter = ("user_name",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("budget", "category_name", "percentage")
    search_fields = ("category_name",)
    list_filter = ("budget",)


class LoansAdmin(admin.ModelAdmin):
    list_display = ("user_name", "loan_name", "amount", "interest_rate", "due_date")
    search_fields = ("loan_name",)
    list_filter = ("user_name",)


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "investment_name", "amount")
    search_fields = ("investment_name",)
    list_filter = ("user_name",)

class InvestmentsThroughTimeAdmin(admin.ModelAdmin):
    list_display = ("date", "amount")
    
class NetWorthAdmin(admin.ModelAdmin):
    list_display = ("user_name", "total_net_worth")
    list_filter = ("user_name",)

admin.site.register(Budget, BudgetAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Loans, LoansAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(InvestmentsThroughTime, InvestmentsThroughTimeAdmin)
admin.site.register(NetWorth)