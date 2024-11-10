from django import forms
from .models import Products

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'available', 'photo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('instance'):
            print(f"Editing product with ID: {kwargs['instance'].id}")

    name = forms.CharField(max_length=200, label="Nombre")
    description = forms.CharField(max_length=300, label="Descripcion")
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio")
    available = forms.BooleanField(initial=True, label="Disponible", required=False)
    photo = forms.ImageField(label="Foto", required=False)

    def save(self, commit=True):
        return super().save(commit=commit)