from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from .models import Order
from .forms import OrderProductForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.


class MyOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/my_order.html'
    context_object_name = "order"

    def get_object(self, queryset= None):
        return Order.objects.filter(is_active=True, user=self.request.user).first()
    
class CreateOrderProductView(LoginRequiredMixin, CreateView):
    template_name = "orders/create_order_product.html"
    form_class = OrderProductForm
    success_url = reverse_lazy("my_order")

    def form_valid(self, form):
        order, _ = Order.objects.get_or_create(
            is_active=True,
            user=self.request.user,
        )
        form.instance.order = order
        form.instance.quantity = 1
        form.save()
        return super().form_valid(form)