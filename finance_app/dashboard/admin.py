from django.contrib import admin
from .models import Budget, Category

# Register your models here.

class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user_name", "budget_name", "amount")
    search_fields = ("budget_name",)
    list_filter = ("user_name",)
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("budget", "category_name", "percentage")
    search_fields = ("category_name",)
    list_filter = ("budget",)
    
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Category, CategoryAdmin)


