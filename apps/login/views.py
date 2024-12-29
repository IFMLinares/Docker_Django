from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from django.shortcuts import redirect
# Create your views here.

class LoginFormVIew(LoginView):
    template_name =  "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:category_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Iniciar Sesión"
        return context

class RedirectView(RedirectView):
    pattern_name = 'auth:login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
