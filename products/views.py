from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import ProductsForm
from django.urls import reverse_lazy
from products.models import Products
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from django.views.generic.edit import UpdateView, DeleteView
# Create your views here.



class ProductFormView(generic.FormView):
    template_name= "admin_dashboard/admin_dashboard.html"
    form_class = ProductsForm
    success_url = reverse_lazy('agregar_producto')


    def form_valid(self, form):
        if not self.request.user.is_superuser:
            return redirect('access_denied')
        form.save()
        return super().form_valid(form)


class ProductListView(generic.ListView):
    template_name = 'products/list_product.html'
    model = Products
    context_object_name = 'products'


class ProductListAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductUpdateView(UpdateView):
    model = Products
    form_class = ProductsForm
    template_name = 'admin_dashboard/admin_update_product.html'
    success_url = reverse_lazy('admin_dashboard')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Products, pk=pk)

    def form_valid(self, form):
        try:
            producto = form.save()
            print(f"Product updated successfully with ID: {producto.id}")
            return redirect('admin_dashboard')
        except Exception as e:
            print(f"Error updating product: {e}")
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        print(f"Form errors: {form.errors}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['producto'] = self.get_object()
        return context

class ProductDeleteView(DeleteView):
    model = Products
    success_url = reverse_lazy('admin_dashboard')
    
    def get(self, request, *args, **kwargs):
        try:
            producto = self.get_object()
            producto.delete()
            return redirect('admin_dashboard')
        except Exception as e:
            print(f"Error deleting product: {e}")
            return redirect('admin_dashboard')
