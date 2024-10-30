from django.contrib import admin
from .models import Products

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    model = Products
    list_display = ['name','price']
    search_fields = ['name']

admin.site.register(Products, ProductAdmin)