from django.contrib.auth import views as auth_views
from django.urls import path
from .views import UserRegistrationView


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login/login.html', next_page='dashboard/'), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]