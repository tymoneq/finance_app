from django.urls import path
from . import views


urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('budget_creation/', views.BudgetView.as_view(), name='budget_creation'),
    path('your_budget/', views.BudgetListView.as_view(), name='your_budget'),
    path('budget/<int:pk>/', views.BudgetDetailView.as_view(), name='budget_detail'),
    path('budget_delete/<int:pk>/', views.BudgetDeleteView.as_view(), name='budget_delete'),
    path('loans/', views.LoanView.as_view(), name='loans'),
    path('loan_delete/<int:pk>/', views.LoanDeleteView.as_view(), name='loan_delete'),
    path('portfolio_creation/', views.PortfolioCreationView.as_view(), name='portfolio_creation'),
    path('net-worth/', views.NetWorthView.as_view(), name='net_worth'),
]