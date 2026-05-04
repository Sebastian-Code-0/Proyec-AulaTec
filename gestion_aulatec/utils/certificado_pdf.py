"""
Generador de PDF para certificados oficiales de la Institución Educativa AulaTec.
Requiere: reportlab
"""
import io
from datetime import datetime


MESES_ES = {
    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
    5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre',
}


def generar_certificado_pdf(certificado):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch, cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table,
            TableStyle, HRFlowable,
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        from reportlab.platypus.flowables import Flowable
    except ImportError:
        raise ImportError('Instala reportlab: pip install reportlab')

    # ── Colores institucionales ──
    PURPLE      = colors.HexColor('#2D1B5E')
    PURPLE_MID  = colors.HexColor('#4A2E8A')
    GOLD        = colors.HexColor('#B8960C')
    GOLD_LIGHT  = colors.HexColor('#F5E6A3')
    GRAY_DARK   = colors.HexColor('#374151')
    GRAY_MID    = colors.HexColor('#6B7280')
    GRAY_LIGHT  = colors.HexColor('#F9FAFB')
    WHITE       = colors.white
    BLACK       = colors.HexColor('#111827')

    # ── Datos del certificado ──
    nombre = certificado.nombre_completo_estudiante or (
        f"{certificado.IdEstudiante.IdUsuario.Nombres} {certificado.IdEstudiante.IdUsuario.Apellidos}"
    )
    documento = certificado.documento_estudiante or certificado.IdEstudiante.IdUsuario.NumId
    grado = certificado.grado_estudiante or 'N/A'
    codigo = certificado.codigo

    if certificado.fecha_aprobacion:
        fecha_obj = certificado.fecha_aprobacion
    else:
        fecha_obj = datetime.now()

    dia   = fecha_obj.day
    mes   = MESES_ES[fecha_obj.month]
    anio  = fecha_obj.year

    tipo_display = {
        'estudio': 'CERTIFICADO DE ESTUDIO',
        'notas':   'CERTIFICADO DE NOTAS',
    }.get(certificado.tipo, 'CERTIFICADO')

    if certificado.tipo == 'estudio':
        cuerpo_texto = (
            f"Que el/la estudiante <b>{nombre}</b>, identificado(a) con documento de identidad "
            f"N.° <b>{documento}</b>, se encuentra matriculado(a) y cursando activamente el grado "
            f"<b>{grado}</b> en esta institución durante el año lectivo <b>{anio}</b>, "
            f"cumpliendo con los requisitos académicos establecidos."
        )
    else:
        cuerpo_texto = (
            f"Que el/la estudiante <b>{nombre}</b>, identificado(a) con documento de identidad "
            f"N.° <b>{documento}</b>, cursó el grado <b>{grado}</b> en esta institución "
            f"durante el año lectivo <b>{anio}</b>, habiendo completado los requisitos "
            f"académicos del periodo correspondiente."
        )

    nombre_admin = ''
    cargo_admin  = 'Rector(a)'
    if certificado.aprobado_por:
        nombre_admin = f"{certificado.aprobado_por.Nombres} {certificado.aprobado_por.Apellidos}"

    # ── Estilos ──
    def estilo(nombre, **kw):
        from reportlab.lib.styles import ParagraphStyle
        return ParagraphStyle(nombre, **kw)

    s_inst    = estilo('inst',    fontName='Helvetica-Bold',    fontSize=15, textColor=PURPLE,     alignment=TA_CENTER, leading=20)
    s_nit     = estilo('nit',     fontName='Helvetica',         fontSize=9,  textColor=GRAY_MID,   alignment=TA_CENTER, leading=13)
    s_resol   = estilo('resol',   fontName='Helvetica-Oblique', fontSize=8,  textColor=GRAY_MID,   alignment=TA_CENTER, leading=12)
    s_tipo    = estilo('tipo',    fontName='Helvetica-Bold',    fontSize=17, textColor=PURPLE_MID, alignment=TA_CENTER, leading=22, spaceBefore=4)
    s_codigo  = estilo('codigo',  fontName='Helvetica',         fontSize=8,  textColor=GRAY_MID,   alignment=TA_CENTER)
    s_certif  = estilo('certif',  fontName='Helvetica-Bold',    fontSize=11, textColor=GRAY_DARK,  alignment=TA_CENTER, leading=16)
    s_cuerpo  = estilo('cuerpo',  fontName='Helvetica',         fontSize=11, textColor=BLACK,       alignment=TA_JUSTIFY, leading=18, spaceBefore=6, spaceAfter=6)
    s_fecha   = estilo('fecha',   fontName='Helvetica',         fontSize=10, textColor=GRAY_DARK,  alignment=TA_CENTER, spaceBefore=10)
    s_firma   = estilo('firma',   fontName='Helvetica-Bold',    fontSize=10, textColor=PURPLE,     alignment=TA_CENTER, leading=14)
    s_cargo   = estilo('cargo',   fontName='Helvetica',         fontSize=9,  textColor=GRAY_MID,   alignment=TA_CENTER)
    s_pie     = estilo('pie',     fontName='Helvetica-Oblique', fontSize=7,  textColor=GRAY_MID,   alignment=TA_CENTER)

    # ── Construcción del documento ──
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
    )

    story = []
    W = letter[0] - 4.4*cm

    # Banda decorativa superior
    story.append(Table(
        [['']],
        colWidths=[W],
        rowHeights=[8],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), PURPLE),
            ('LINEBELOW',  (0,0), (-1,-1), 3, GOLD),
        ])
    ))
    story.append(Spacer(1, 16))

    # Encabezado institución
    story.append(Paragraph(certificado.nombre_institucion.upper(), s_inst))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"NIT: {certificado.nit_institucion}", s_nit))
    story.append(Paragraph(certificado.resolucion, s_resol))
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width='100%', thickness=2, color=GOLD, spaceAfter=10))

    # Título
    story.append(Paragraph(tipo_display, s_tipo))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"Código: {codigo}", s_codigo))
    story.append(Spacer(1, 14))

    story.append(HRFlowable(width='80%', thickness=0.5, color=colors.HexColor('#D1D5DB'), spaceAfter=14))

    story.append(Paragraph("La Institución Educativa AulaTec", s_certif))
    story.append(Paragraph("<b>CERTIFICA QUE:</b>", s_certif))
    story.append(Spacer(1, 18))

    # Cuerpo con borde dorado izquierdo
    cuerpo_table = Table(
        [[Paragraph(cuerpo_texto, s_cuerpo)]],
        colWidths=[W],
        style=TableStyle([
            ('LINEBEFORE',    (0,0), (0,-1), 3, GOLD),
            ('LEFTPADDING',   (0,0), (-1,-1), 14),
            ('RIGHTPADDING',  (0,0), (-1,-1), 8),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('BACKGROUND',    (0,0), (-1,-1), GOLD_LIGHT),
            ('ROUNDEDCORNERS', [4]),
        ])
    )
    story.append(cuerpo_table)
    story.append(Spacer(1, 24))

    # Fecha de expedición
    story.append(Paragraph(
        f"El presente certificado se expide a solicitud del interesado(a) a los "
        f"<b>{dia}</b> días del mes de <b>{mes}</b> del año <b>{anio}</b>.",
        s_fecha
    ))

    if certificado.fecha_vencimiento:
        fv = certificado.fecha_vencimiento
        story.append(Paragraph(
            f"Válido hasta el {fv.day} de {MESES_ES[fv.month]} de {fv.year}.",
            s_fecha
        ))

    story.append(Spacer(1, 36))

    # Firma
    firma_linea = Table(
        [
            [HRFlowable(width='55%', thickness=1, color=PURPLE_MID)],
            [Paragraph(nombre_admin if nombre_admin else '___________________________', s_firma)],
            [Paragraph(cargo_admin, s_cargo)],
            [Paragraph(certificado.nombre_institucion, s_cargo)],
        ],
        colWidths=[W],
        style=TableStyle([
            ('ALIGN',  (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ])
    )
    story.append(firma_linea)
    story.append(Spacer(1, 28))

    # Pie de página
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#D1D5DB'), spaceAfter=6))
    story.append(Paragraph(
        f"Documento generado digitalmente por el sistema AulaTec · "
        f"Código de verificación: {codigo} · "
        f"Generado el {dia} de {mes} de {anio}",
        s_pie
    ))

    # Banda decorativa inferior
    story.append(Spacer(1, 6))
    story.append(Table(
        [['']],
        colWidths=[W],
        rowHeights=[6],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), PURPLE),
            ('LINEABOVE',  (0,0), (-1,-1), 2, GOLD),
        ])
    ))

    doc.build(story)
    return buffer.getvalue()
