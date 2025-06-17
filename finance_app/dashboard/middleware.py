from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve


EXEMPT_URLS = [
   'dashboard'
]  # URL names (not paths)

# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         current_url_name = resolve(request.path_info).url_name
#         if not request.user.is_authenticated and current_url_name not in EXEMPT_URLS:
#             return redirect(f'{settings.LOGIN_URL}?next={request.path}')
#         return self.get_response(request)