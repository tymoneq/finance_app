from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import  login, logout
from django.http import HttpResponseRedirect

from django.views import View


# Create your views here.
class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "login/register.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
        return render(request, "login/register.html", {"form": form})
