from django.db import models
from django.contrib.auth.models import User
from products.models import Products
from reportlab.lib import colors
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from datetime import datetime
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    order_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"order {self.id} by {self.user}"
    
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.orderproduct_set.all())
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()


    def __str__(self):
        return f"{self.order} - {self.product}"
    

class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.order.user.username}"
    
    def generar_ticket_pdf(self):
        numero_ticket = datetime.now().strftime("%Y%m%d%H%M")
        
        archivo_pdf = "ticket.pdf"
        c = canvas.Canvas(archivo_pdf, pagesize=(80 * mm, 200 * mm))
        c.setFont("Helvetica", 8)

        y = 190 * mm

        # Encabezado
        c.drawString(10 * mm, y, "Supermercado Ejemplo")
        y -= 10 * mm
        c.drawString(10 * mm, y, f"Ticket No: {numero_ticket}")
        y -= 10 * mm

        # Cliente
        c.drawString(10 * mm, y, f"Cliente: {self.order.user.username}")
        y -= 10 * mm

        # Productos
        c.drawString(10 * mm, y, "Productos:")
        y -= 10 * mm
        for item in self.order.orderproduct_set.all():
            producto = item.product
            cantidad = item.quantity
            subtotal = producto.price * cantidad
            c.drawString(10 * mm, y, f"{producto.name} (x{cantidad})")
            c.drawRightString(70 * mm, y, f"${subtotal:.2f}")
            y -= 10 * mm

        # Línea divisoria
        c.drawString(10 * mm, y, "------------------------")
        y -= 10 * mm

        # Total
        total = self.order.get_total_price()
        c.drawString(10 * mm, y, "Total:")
        c.drawRightString(70 * mm, y, f"${total:.2f}")
        y -= 20 * mm

        # Mensaje de despedida
        c.drawString(10 * mm, y, "Gracias por su compra!")
        y -= 10 * mm
        c.drawString(10 * mm, y, "Vuelva pronto")

        # Guardar PDF
        c.save()
        return archivo_pdf

