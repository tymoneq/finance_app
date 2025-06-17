from django.urls import path
from . import views


urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('budget_creation/', views.BudgetView.as_view(), name='budget_creation'),
    path('your_budget/', views.BudgetListView.as_view(), name='your_budget'),
    path('credit/', views.CreditView.as_view(), name='credit'),
    path('investments/', views.InvestmentsView.as_view(), name='investments'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('net-worth/', views.NetWorthView.as_view(), name='net_worth'),
]