from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser
from django.conf import settings
from django.views.generic import TemplateView
from products.forms import ProductsForm
from products.models import Products

# Create your views here.

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")


class AdminLoginView(LoginView):
    template_name = "admin_dashboard/admin_login.html"

    def get_success_url(self):

        return getattr(settings, 'LOGIN_ADMIN_REDIRECT', reverse_lazy("admin_dashboard"))

    def form_valid(self, form):

        if not self.request.user.is_superuser:

            return redirect('access_denied')
        return super().form_valid(form)



class AdminDashboardView(TemplateView):
    template_name = 'admin_dashboard/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductsForm()
        context['products'] = Products.objects.all()
        return context

