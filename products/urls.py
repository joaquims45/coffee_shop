"""
URL configuration for coffee_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from .views import ProductFormView, ProductListView, ProductListAPI, ProductUpdateView, ProductDeleteView


urlpatterns = [
    path('agregar', ProductFormView.as_view(), name="agregar_producto"),
    path('productos/editar/<int:pk>/', ProductUpdateView.as_view(), name='editar_producto'),
    path('eliminar/<int:pk>/', ProductDeleteView.as_view(), name="borrar_producto"),
    path('api/', ProductListAPI.as_view(), name='list_products_api'),
    path('list/', ProductListView.as_view(), name='list_product' ),
]
