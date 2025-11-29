from django.shortcuts import render, redirect, get_object_or_404
from gestion_aulatec.models.certificado import Certificado
from django.http import HttpResponse, Http404
from ..models.estudiante import Estudiante
from ..models.materia import Materia
from ..models.usuario import Usuario
from django.contrib.auth.decorators import login_required
import os
from io import BytesIO
from datetime import datetime

# Importaciones de ReportLab para PDF mejorado
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image


def test_view(request):
    return HttpResponse("<h1>FUNCIONA! Esta es la vista de certificados</h1>")


# ==================== VISTAS CRUD ====================

def certificado_list(request):
    """Lista todos los certificados (para admin)"""
    certificados = Certificado.objects.all()
    return render(request, 'gestion_aulatec/certificado_list.html', {'certificados': certificados})


def certificado_create(request):
    """Crear un nuevo certificado (para admin)"""
    estudiantes = Estudiante.objects.all()
    materias = Materia.objects.all()
    usuarios = Usuario.objects.all()

    if request.method == "POST":
        estudiante = Estudiante.objects.get(IdEstudiante=request.POST["estudiante"])
        materia = Materia.objects.get(IdMateria=request.POST["materia"])
        usuario = Usuario.objects.get(IdUsuario=request.POST["usuario"])
        tipo = request.POST["tipo"]

        # Crear código único con timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        codigo = f"CERT-{estudiante.IdEstudiante}-{materia.IdMateria}-{timestamp}"

        # Crear el registro en BD
        certificado = Certificado.objects.create(
            IdEstudiante=estudiante,
            IdMateria=materia,
            IdUsuario=usuario,
            tipo=tipo,
            codigo=codigo
        )

        return redirect("gestion_aulatec:certificado_list")

    return render(request, "gestion_aulatec/certificado_form.html", {
        "estudiantes": estudiantes,
        "materias": materias,
        "usuarios": usuarios
    })


def certificado_detail(request, pk):
    """Ver detalles de un certificado"""
    certificado = get_object_or_404(Certificado, pk=pk)
    return render(request, 'gestion_aulatec/certificado_detail.html', {'certificado': certificado})


def certificado_delete(request, pk):
    """Eliminar un certificado"""
    certificado = get_object_or_404(Certificado, pk=pk)
    certificado.delete()
    return redirect('gestion_aulatec:certificado_list')


def certificado_preview(request, id):
    """Vista previa HTML del certificado"""
    cert = get_object_or_404(Certificado, IdCertificado=id)
    return render(request, 'gestion_aulatec/certificado_preview.html', {'cert': cert})


# ==================== VISTAS DE DESCARGA PDF ====================

@login_required
def descargar_mi_certificado(request, pk):
    """
    Vista para que un ESTUDIANTE descargue SU PROPIO certificado
    Verifica que el certificado pertenezca al estudiante logueado
    """
    cert = get_object_or_404(Certificado, IdCertificado=pk)
    
    # Verificar que el certificado pertenece al estudiante logueado
    try:
        estudiante = Estudiante.objects.get(IdUsuario=request.user)
        if cert.IdEstudiante != estudiante:
            raise Http404("No tienes permiso para descargar este certificado.")
    except Estudiante.DoesNotExist:
        raise Http404("No tienes un perfil de estudiante.")
    
    # Generar y retornar el PDF
    return generar_pdf_certificado(cert)


def certificado_pdf(request, pk):
    """
    Vista para que el ADMIN descargue cualquier certificado
    Sin restricciones de permisos
    """
    cert = get_object_or_404(Certificado, IdCertificado=pk)
    return generar_pdf_certificado(cert)


# ==================== FUNCIÓN GENERADORA DE PDF ====================

def generar_pdf_certificado(cert):
    """
    Función reutilizable que genera el PDF del certificado
    Incluye: Nombre, Tipo Doc, Número Doc, NIT, Código, etc.
    """
    # Validar datos necesarios
    if not cert.IdEstudiante or not cert.IdEstudiante.IdUsuario:
        return HttpResponse("Error: Este certificado no tiene datos del estudiante.", status=400)
    
    # Crear buffer en memoria
    buffer = BytesIO()
    
    # Configurar documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=50,
        bottomMargin=50,
    )
    
    # Lista para almacenar elementos del PDF
    elements = []
    
    # Obtener estilos predeterminados
    styles = getSampleStyleSheet()
    
    # ===== ESTILOS PERSONALIZADOS =====
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        leading=18
    )
    
    nombre_destacado = ParagraphStyle(
        'NombreDestacado',
        parent=styles['Normal'],
        fontSize=20,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    # ===== CONTENIDO DEL PDF =====
    
    # Logo del colegio (si existe)
    logo_path = 'gestion_aulatec/static/gestion_aulatec/img/logo_colegio.png'
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=2*inch, height=2*inch)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 0.3*inch))
        except:
            pass  # Si no existe el logo, continuar sin él
    
    # Título principal
    elements.append(Paragraph("CERTIFICADO DE ESTUDIO", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Línea decorativa
    line_data = [['', '', '']]
    line_table = Table(line_data, colWidths=[2*inch, 2*inch, 2*inch])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 3, colors.HexColor('#c9a42a')),
        ('LINEBELOW', (0, 0), (-1, 0), 3, colors.HexColor('#c9a42a')),
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Nombre de la institución y NIT
    elements.append(Paragraph("INSTITUCIÓN EDUCATIVA AULATEC", subtitle_style))
    elements.append(Spacer(1, 0.05*inch))
    nit_text = f"NIT: {cert.nit_institucion}"
    elements.append(Paragraph(nit_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    resolucion_text = "Resolución No. 06-021-2021 de la S.E.D"
    elements.append(Paragraph("Certifica que:", body_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Nombre del estudiante destacado
    estudiante_nombre = f"{cert.IdEstudiante.IdUsuario.Nombres} {cert.IdEstudiante.IdUsuario.Apellidos}"
    elements.append(Paragraph(estudiante_nombre.upper(), nombre_destacado))
    
    # Línea decorativa bajo el nombre
    elements.append(Spacer(1, 0.1*inch))
    name_line = Table([['']], colWidths=[4*inch])
    name_line.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#c9a42a')),
    ]))
    elements.append(name_line)
    elements.append(Spacer(1, 0.3*inch))
    
    # Información del estudiante
    tipo_doc = cert.IdEstudiante.IdUsuario.TipoId if cert.IdEstudiante.IdUsuario.TipoId else "N/A"
    num_doc = cert.IdEstudiante.IdUsuario.NumId if cert.IdEstudiante.IdUsuario.NumId else "N/A"
    
    info_estudiante = f"""
    Identificado(a) con <b>{tipo_doc}</b> número <b>{num_doc}</b>, 
    ha sido estudiante de esta institución y ha cumplido satisfactoriamente 
    con los requisitos académicos establecidos.
    """
    elements.append(Paragraph(info_estudiante, body_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Si tiene materia asociada
    if cert.IdMateria:
        texto_materia = f"""
        Certificado otorgado para el área de <b>{cert.IdMateria.NombreMateria}</b>.
        """
        elements.append(Paragraph(texto_materia, body_style))
        elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de información del certificado
    fecha = cert.fecha_emision.strftime('%d de %B de %Y') if cert.fecha_emision else "N/A"
    
    data = [
        ['Tipo de Documento:', tipo_doc],
        ['Número de Identificación:', num_doc],
        ['Tipo de Certificado:', cert.tipo if cert.tipo else 'N/A'],
        ['Código del Certificado:', cert.codigo if cert.codigo else 'N/A'],
        ['Fecha de Emisión:', fecha],
        ['Estado:', cert.estado.upper() if cert.estado else 'ACTIVO'],
    ]
    
    info_table = Table(data, colWidths=[2.8*inch, 2.7*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.6*inch))
    
    # Sección de firmas
    firma_data = [
        ['_________________________', '_________________________'],
        ['Director(a)', 'Secretario(a) Académico'],
        ['Institución Educativa AulaTec', 'Área de Certificaciones']
    ]
    
    firma_table = Table(firma_data, colWidths=[2.5*inch, 2.5*inch])
    firma_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 20),
    ]))
    elements.append(firma_table)
    
    # Pie de página con código de verificación
    elements.append(Spacer(1, 0.4*inch))
    footer_text = f"«Este certificado es válido para trámites oficiales» - Código de verificación: {cert.codigo}"
    elements.append(Paragraph(footer_text, footer_style))
    
    # Construir el PDF
    doc.build(elements)
    
    # Obtener el contenido del PDF del buffer
    pdf_output = buffer.getvalue()
    buffer.close()
    
    # Crear respuesta HTTP con el PDF
    response = HttpResponse(pdf_output, content_type='application/pdf')
    filename = f"certificado_{cert.IdEstudiante.IdUsuario.NumId}_{cert.codigo}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response