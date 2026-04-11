"""
Generador de PDF para certificados.
Requiere: pip install reportlab
"""
import io


def generar_certificado_pdf(certificado):
    """
    Genera el PDF de un certificado y devuelve los bytes del archivo.
    Requiere reportlab instalado: pip install reportlab
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
    except ImportError:
        raise ImportError(
            "Para generar PDFs instala reportlab: pip install reportlab"
        )

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # ── Encabezado institución ──
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 1.5 * inch, certificado.nombre_institucion)

    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 1.85 * inch, f"NIT: {certificado.nit_institucion}")
    c.drawCentredString(width / 2, height - 2.1 * inch, certificado.resolucion)

    # ── Línea separadora ──
    c.line(inch, height - 2.35 * inch, width - inch, height - 2.35 * inch)

    # ── Título del certificado ──
    tipo_display = {
        'estudio': 'CERTIFICADO DE ESTUDIO',
        'notas': 'CERTIFICADO DE NOTAS',
        'conducta': 'CERTIFICADO DE CONDUCTA',
    }.get(certificado.tipo, 'CERTIFICADO')

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 2.85 * inch, tipo_display)

    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, height - 3.1 * inch, f"Código: {certificado.codigo}")

    # ── Cuerpo ──
    c.setFont("Helvetica", 12)
    y = height - 3.75 * inch
    line_h = 0.35 * inch

    nombre = certificado.nombre_completo_estudiante or (
        f"{certificado.IdEstudiante.IdUsuario.Nombres} {certificado.IdEstudiante.IdUsuario.Apellidos}"
    )
    documento = certificado.documento_estudiante or certificado.IdEstudiante.IdUsuario.NumId
    grado = certificado.grado_estudiante or "N/A"

    c.drawString(inch, y, "La Institución Educativa AulaTec certifica que:")
    y -= line_h

    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, y, nombre)
    y -= line_h

    c.setFont("Helvetica", 12)
    c.drawString(inch, y, f"Identificado(a) con documento No. {documento},")
    y -= line_h
    c.drawString(inch, y, f"cursó satisfactoriamente el grado {grado} en esta institución.")
    y -= line_h * 1.5

    if certificado.observaciones:
        c.setFont("Helvetica-Oblique", 11)
        c.drawString(inch, y, f"Observaciones: {certificado.observaciones}")
        y -= line_h * 1.5

    # ── Fecha de expedición ──
    c.setFont("Helvetica", 12)
    if certificado.fecha_aprobacion:
        from django.utils.formats import date_format
        fecha_str = certificado.fecha_aprobacion.strftime("%d de %B de %Y")
    else:
        from datetime import datetime
        fecha_str = datetime.now().strftime("%d de %B de %Y")
    c.drawString(inch, y, f"Se expide el {fecha_str}.")

    # ── Firma ──
    y -= 1.75 * inch
    c.line(inch, y, 3.5 * inch, y)
    y -= 0.25 * inch
    c.setFont("Helvetica", 10)
    if certificado.aprobado_por:
        nombre_admin = f"{certificado.aprobado_por.Nombres} {certificado.aprobado_por.Apellidos}"
        c.drawString(inch, y, nombre_admin)
        y -= 0.2 * inch
    c.drawString(inch, y, "Coordinador(a) Académico(a)")

    c.save()
    return buffer.getvalue()
