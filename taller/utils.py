import io
import os
from django.conf import settings
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generar_pdf_y_enviar_correo(servicio, email_cliente):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    ancho, alto = letter

   
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, alto - 50, "TALLER RÁPIDO JUÁREZ")
    p.setFont("Helvetica", 10)
    p.drawString(50, alto - 70, "Comprobante de Servicio Técnico")
    p.drawString(50, alto - 85, f"Ticket N°: {servicio.id} | Fecha: {servicio.fecha_agenda.strftime('%d/%m/%Y')}")
    
   
    p.line(50, alto - 100, ancho - 50, alto - 100)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, alto - 120, "Datos del Vehículo:")
    p.setFont("Helvetica", 10)
    p.drawString(50, alto - 140, f"Patente: {servicio.auto.placa}")
    p.drawString(50, alto - 155, f"Vehículo: {servicio.auto.marca} {servicio.auto.modelo} ({servicio.auto.anio})")
    p.drawString(50, alto - 170, f"Km Ingreso: {servicio.km_entrada} km")
    
    p.drawString(ancho / 2, alto - 140, f"Cliente: {servicio.auto.cliente.nombre}")
    p.drawString(ancho / 2, alto - 155, f"Mecánico: {servicio.mecanico.nombre if servicio.mecanico else 'Sin asignar'}")

    
    p.line(50, alto - 190, ancho - 50, alto - 190)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, alto - 210, "Desglose Financiero:")
    p.setFont("Helvetica", 10)
    
    y = alto - 230
    p.drawString(50, y, "Mano de Obra (Neto):")
    p.drawRightString(ancho - 50, y, f"${servicio.costo_mano_obra_neto}")
    
    y -= 20
    p.drawString(50, y, "Refacciones (Neto):")
    y -= 15
    for detalle in servicio.refacciones_usadas.all():
        p.drawString(70, y, f"- {detalle.cantidad}x {detalle.refaccion.nombre}")
        subtotal_ref = detalle.cantidad * detalle.precio_unitario_neto
        p.drawRightString(ancho - 50, y, f"${subtotal_ref}")
        y -= 15
    
    
    y -= 10
    p.line(50, y, ancho - 50, y)
    y -= 20
    p.drawString(50, y, "Subtotal:")
    p.drawRightString(ancho - 50, y, f"${servicio.subtotal_neto}")
    
    y -= 15
    p.drawString(50, y, f"IVA ({servicio.porcentaje_iva_aplicado}%):")
    p.drawRightString(ancho - 50, y, f"${servicio.iva_total}")
    
    y -= 25
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "TOTAL A PAGAR:")
    p.drawRightString(ancho - 50, y, f"${servicio.gran_total}")
    
    
    y -= 100
    ruta_firma = os.path.join(settings.BASE_DIR, 'taller', 'static', 'firmas', 'firma.png')
    
    if os.path.exists(ruta_firma):
        
        p.drawImage(ruta_firma, 50, y, width=225, height=75, mask='auto')
        y -= 20
        p.setFont("Helvetica-Oblique", 9)
        p.drawString(50, y, "Firma Autorizada - Taller Juárez")
    else:
        p.line(50, y + 10, 200, y + 10)
        p.drawString(50, y, "(Firma no disponible)")

    p.showPage()
    p.save()
    
    pdf_generado = buffer.getvalue()
    buffer.close()

    mensaje_correo = f"""
    Hola {servicio.auto.cliente.nombre},
    
    Tu vehículo {servicio.auto.marca} {servicio.auto.modelo} (Patente: {servicio.auto.placa}) ya está TERMINADO.
    Adjuntamos el comprobante detallado. El total es de ${servicio.gran_total}.
    
    ¡Te esperamos para el retiro!
    """

    email = EmailMessage(
        subject=f"Vehículo Listo - Taller Juárez (Ticket #{servicio.id})",
        body=mensaje_correo,
        from_email=os.getenv('EMAIL_HOST_USER'),
        to=[email_cliente],
    )
    email.attach(f"Factura_Taller_{servicio.id}.pdf", pdf_generado, "application/pdf")
    email.send(fail_silently=False)