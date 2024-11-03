from django.urls import path, include
from .views import MyOrderView, CreateOrderProductView, generar_ticket_pdf

urlpatterns = [
    path('mi-orden', MyOrderView.as_view(), name="my_order"),
    path('agregar-producto', CreateOrderProductView.as_view(), name='add_product'),
    path('generar-ticket/<int:ticket_id>', generar_ticket_pdf, name='generate_ticket')
]
