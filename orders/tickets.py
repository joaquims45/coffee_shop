from reportlab.lib.pagesizes import receipt
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime

def generar_ticket_pdf(order):
    numero_ticket = datetime.now().strftime("%Y%m%d%H%M")
    
    archivo_pdf = "ticket.pdf"
    c = canvas.Canvas(archivo_pdf, pagesize=(80 * mm, 200 * mm))
    c.setFont("Helvetica", 8)

    y = 190 * mm

    c.drawString(10 * mm, y, "Supermercado Ejemplo")
    y -= 10
    c.drawString(10 * mm, y, f"Ticket No: {numero_ticket}")
    y -= 10

    c.drawString(10 * mm, y, f"Cliente: {order.user.username}")
    y -= 10

    c.drawString(10 * mm, y, "Productos:")
    y -= 10
    for item in order.orderproduct_set.all():
        producto = item.product
        cantidad = item.quantity
        subtotal = producto.price * cantidad
        c.drawString(10 * mm, y, f"{producto.name} (x{cantidad})")
        c.drawRightString(70 * mm, y, f"${subtotal:.2f}")
        y -= 10

    c.drawString(10 * mm, y, "------------------------")
    y -= 10

    total = order.get_total_price()
    c.drawString(10 * mm, y, "Total:")
    c.drawRightString(70 * mm, y, f"${total:.2f}")
    y -= 20

    c.drawString(10 * mm, y, "Gracias por su compra!")
    y -= 10
    c.drawString(10 * mm, y, "Vuelva pronto")

    c.save()
    return archivo_pdf
