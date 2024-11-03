from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, TemplateView
from .models import Order
from .forms import OrderProductForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from datetime import datetime
from .models import Ticket
import os
from django.conf import settings


# Create your views here.


class MyOrderView(TemplateView):
    template_name = 'orders/my_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.filter(
            user=self.request.user, 
            is_active=True
        ).first()
        
        if order:
            # Obtener o crear el ticket para esta orden
            ticket, created = Ticket.objects.get_or_create(order=order)
            context['ticket'] = ticket
            
        context['order'] = order
        return context

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

def generar_ticket_pdf(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    numero_ticket = datetime.now().strftime("%Y%m%d%H%M")
    
    # Crear el directorio si no existe
    tickets_dir = os.path.join(settings.MEDIA_ROOT, 'tickets')
    os.makedirs(tickets_dir, exist_ok=True)
    
    # Crear la ruta completa del archivo
    archivo_pdf = os.path.join(tickets_dir, f'ticket_{ticket.id}_{numero_ticket}.pdf')
    
    c = canvas.Canvas(archivo_pdf, pagesize=(80 * mm, 200 * mm))
    c.setFont("Helvetica", 8)

    y = 190 * mm

    c.drawString(10 * mm, y, "Coffee Shop")
    y -= 10 * mm
    c.drawString(10 * mm, y, f"Ticket No: {numero_ticket}")
    y -= 10 * mm

    c.drawString(10 * mm, y, f"Cliente: {ticket.order.user.username}")
    y -= 10 * mm

    c.drawString(10 * mm, y, "Productos:")
    y -= 10 * mm
    for item in ticket.order.orderproduct_set.all():
        producto = item.product
        cantidad = item.quantity
        subtotal = producto.price * cantidad
        c.drawString(10 * mm, y, f"{producto.name} (x{cantidad})")
        c.drawRightString(70 * mm, y, f"${subtotal:.2f}")
        y -= 10 * mm

    c.drawString(10 * mm, y, "------------------------")
    y -= 10 * mm

    total = ticket.order.total_price()   
    c.drawString(10 * mm, y, "Total:")
    c.drawRightString(70 * mm, y, f"${total:.2f}")
    y -= 20 * mm

    c.drawString(10 * mm, y, "Gracias por su compra!")
    y -= 10 * mm
    c.drawString(10 * mm, y, "Vuelva pronto")

    c.save()
    
    # Abrir y devolver el archivo PDF
    pdf = open(archivo_pdf, 'rb')
    response = FileResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}_{numero_ticket}.pdf"'
    return response