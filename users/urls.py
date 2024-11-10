from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, AdminLoginView, AdminDashboardView
from django.urls import path

urlpatterns = [
     path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
     path("logout/", LogoutView.as_view(), name="logout"),
     path("registro/", RegisterView.as_view(), name="register"),
     path("admin_login/", AdminLoginView.as_view(), name="admin_login"),
     path("admin_dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
]
