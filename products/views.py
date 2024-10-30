from django.shortcuts import render
from django.views import generic
from .forms import ProductsForm
from django.urls import reverse_lazy
from products.models import Products
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
# Create your views here.



class ProductFormView(generic.FormView):
    template_name= "products/add_product.html"
    form_class = ProductsForm
    success_url = reverse_lazy('add_product')

    def form_valid(self, form):
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
