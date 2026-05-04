"""
Generador de PDF de reporte de notas académicas con gráficas.
Requiere: reportlab, matplotlib
"""
import io
import matplotlib
matplotlib.use('Agg')  # Backend sin pantalla, obligatorio en servidor
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def _fig_a_bytes(fig):
    """Convierte una figura matplotlib a bytes PNG en memoria."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def generar_reporte_notas_pdf(estudiante, calificaciones, anio):
    """
    Genera el PDF de reporte de notas con gráficas.

    Parámetros:
        estudiante   — instancia de Estudiante (con IdUsuario e IdGrado)
        calificaciones — queryset de Calificacion del estudiante
        anio         — año lectivo (int)

    Retorna: bytes del PDF
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch, cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Image,
            Table, TableStyle, PageBreak, HRFlowable,
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.platypus.flowables import KeepTogether
    except ImportError:
        raise ImportError('Instala reportlab: pip install reportlab')

    try:
        from gestion_aulatec.models import Calificacion
        from django.db.models import Avg
    except Exception:
        pass

    # ── Paleta de colores ──
    PURPLE       = colors.HexColor('#3B1F6E')
    PURPLE_LIGHT = colors.HexColor('#6D4FA0')
    PURPLE_PALE  = colors.HexColor('#EDE9F8')
    ACCENT       = colors.HexColor('#06B6D4')
    SUCCESS      = colors.HexColor('#10B981')
    WARNING      = colors.HexColor('#F59E0B')
    DANGER       = colors.HexColor('#EF4444')
    GRAY_LIGHT   = colors.HexColor('#F3F4F6')
    GRAY         = colors.HexColor('#9CA3AF')
    WHITE        = colors.white
    BLACK        = colors.HexColor('#111827')

    # ── Estilos ──
    styles = getSampleStyleSheet()

    def estilo(nombre, **kwargs):
        return ParagraphStyle(nombre, parent=styles['Normal'], **kwargs)

    s_titulo     = estilo('titulo',     fontSize=20, textColor=PURPLE,       fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)
    s_subtitulo  = estilo('subtitulo',  fontSize=11, textColor=PURPLE_LIGHT, fontName='Helvetica',      alignment=TA_CENTER, spaceAfter=2)
    s_seccion    = estilo('seccion',    fontSize=12, textColor=PURPLE,       fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6)
    s_normal     = estilo('snormal',    fontSize=9,  textColor=BLACK,        fontName='Helvetica')
    s_muted      = estilo('smuted',     fontSize=8,  textColor=GRAY,         fontName='Helvetica')
    s_center     = estilo('scenter',    fontSize=9,  textColor=BLACK,        fontName='Helvetica', alignment=TA_CENTER)
    s_bold       = estilo('sbold',      fontSize=9,  textColor=BLACK,        fontName='Helvetica-Bold')
    s_verde      = estilo('sverde',     fontSize=9,  textColor=SUCCESS,      fontName='Helvetica-Bold', alignment=TA_CENTER)
    s_rojo       = estilo('srojo',      fontSize=9,  textColor=DANGER,       fontName='Helvetica-Bold', alignment=TA_CENTER)
    s_amarillo   = estilo('samarillo',  fontSize=9,  textColor=WARNING,      fontName='Helvetica-Bold', alignment=TA_CENTER)

    # ── Datos base ──
    from django.db.models import Avg, Count
    from gestion_aulatec.models import Calificacion as Cal

    nombre_est  = f"{estudiante.IdUsuario.Nombres} {estudiante.IdUsuario.Apellidos}"
    doc_est     = estudiante.IdUsuario.NumId
    grado_est   = f"{estudiante.IdGrado.NumGrado}° {estudiante.IdGrado.NumCurso}" if estudiante.IdGrado else 'Sin asignar'

    periodos_nombres = {1: 'Primer Periodo', 2: 'Segundo Periodo', 3: 'Tercer Periodo', 4: 'Cuarto Periodo'}

    # Promedios del estudiante por materia
    promedios_materia = {}
    materias_ids = calificaciones.values_list('IdMateria', flat=True).distinct()
    from gestion_aulatec.models import Materia
    for mid in materias_ids:
        avg = calificaciones.filter(IdMateria=mid).aggregate(Avg('Nota'))['Nota__avg']
        nombre_mat = calificaciones.filter(IdMateria=mid).first().IdMateria.NombreMateria
        if avg is not None:
            promedios_materia[nombre_mat] = round(float(avg), 2)

    # Promedio del salón por materia (todos los estudiantes del mismo grado)
    promedios_salon = {}
    if estudiante.IdGrado:
        from gestion_aulatec.models import Estudiante as Est
        compañeros = Est.objects.filter(IdGrado=estudiante.IdGrado).values_list('IdEstudiante', flat=True)
        for nombre_mat, _ in promedios_materia.items():
            mat_obj = calificaciones.filter(IdMateria__NombreMateria=nombre_mat).first().IdMateria
            avg_salon = Cal.objects.filter(
                IdEstudiante__in=compañeros,
                IdMateria=mat_obj,
                AnioLectivo=anio,
            ).aggregate(Avg('Nota'))['Nota__avg']
            promedios_salon[nombre_mat] = round(float(avg_salon), 2) if avg_salon else None

    # Promedios por periodo
    promedios_periodo = {}
    for p in range(1, 5):
        avg = calificaciones.filter(Periodo=p).aggregate(Avg('Nota'))['Nota__avg']
        promedios_periodo[p] = round(float(avg), 2) if avg else None

    promedio_general = round(
        sum(v for v in promedios_periodo.values() if v) /
        max(len([v for v in promedios_periodo.values() if v]), 1), 2
    )

    # Clasificar materias
    mat_ordenadas = sorted(promedios_materia.items(), key=lambda x: x[1], reverse=True)
    mejores   = [m for m in mat_ordenadas if m[1] >= 7.0][:3]
    a_mejorar = [m for m in mat_ordenadas if m[1] < 6.0][:3]

    # ── Colores matplotlib consistentes con la paleta ──
    COLOR_EST   = '#3B1F6E'
    COLOR_SALON = '#06B6D4'
    BG_FIG      = '#FAFAFA'

    # ────────────────────────────────────────────────
    # GRÁFICA 1 — Promedios por periodo (línea)
    # ────────────────────────────────────────────────
    periodos_con_datos = [(p, v) for p, v in promedios_periodo.items() if v is not None]
    fig1, ax1 = plt.subplots(figsize=(6.5, 3), facecolor=BG_FIG)
    ax1.set_facecolor(BG_FIG)

    if periodos_con_datos:
        xs = [p for p, _ in periodos_con_datos]
        ys = [v for _, v in periodos_con_datos]
        ax1.plot(xs, ys, 'o-', color=COLOR_EST, linewidth=2.5, markersize=8, zorder=3)
        ax1.fill_between(xs, ys, alpha=0.12, color=COLOR_EST)
        for x, y in zip(xs, ys):
            ax1.annotate(f'{y}', (x, y), textcoords='offset points',
                         xytext=(0, 10), ha='center', fontsize=10, fontweight='bold', color=COLOR_EST)
        ax1.axhline(y=6.0, color='#EF4444', linestyle='--', linewidth=1, alpha=0.6, label='Mínimo aprobatorio (6.0)')
        ax1.set_ylim(0, 10.5)
        ax1.set_xlim(0.5, 4.5)
        ax1.set_xticks([1, 2, 3, 4])
        ax1.set_xticklabels(['P1', 'P2', 'P3', 'P4'], fontsize=10)
        ax1.set_ylabel('Promedio', fontsize=9)
        ax1.legend(fontsize=8, framealpha=0.5)
    else:
        ax1.text(0.5, 0.5, 'Sin datos de calificaciones', ha='center', va='center',
                 transform=ax1.transAxes, fontsize=11, color='#9CA3AF')

    ax1.set_title('Evolución de promedios por periodo', fontsize=11, fontweight='bold', color=COLOR_EST, pad=10)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    fig1.tight_layout()
    img1_bytes = _fig_a_bytes(fig1)

    # ────────────────────────────────────────────────
    # GRÁFICA 2 — Comparativa estudiante vs salón por materia (barras)
    # ────────────────────────────────────────────────
    materias_graf = list(promedios_materia.keys())
    vals_est   = [promedios_materia[m] for m in materias_graf]
    vals_salon = [promedios_salon.get(m) for m in materias_graf]

    fig2, ax2 = plt.subplots(figsize=(6.5, max(3, len(materias_graf) * 0.55 + 1)), facecolor=BG_FIG)
    ax2.set_facecolor(BG_FIG)

    if materias_graf:
        y_pos = np.arange(len(materias_graf))
        bar_h = 0.35

        bars_est = ax2.barh(y_pos + bar_h/2, vals_est, bar_h,
                            label='Tu promedio', color=COLOR_EST, alpha=0.85, zorder=3)
        if any(v is not None for v in vals_salon):
            salon_clean = [v if v is not None else 0 for v in vals_salon]
            ax2.barh(y_pos - bar_h/2, salon_clean, bar_h,
                     label='Promedio del salón', color=COLOR_SALON, alpha=0.7, zorder=3)

        for bar in bars_est:
            w = bar.get_width()
            ax2.text(w + 0.1, bar.get_y() + bar.get_height()/2,
                     f'{w}', va='center', fontsize=8, fontweight='bold', color=COLOR_EST)

        ax2.axvline(x=6.0, color='#EF4444', linestyle='--', linewidth=1, alpha=0.5)
        ax2.set_yticks(y_pos)
        etiquetas = [m if len(m) <= 18 else m[:16] + '…' for m in materias_graf]
        ax2.set_yticklabels(etiquetas, fontsize=8)
        ax2.set_xlim(0, 11)
        ax2.set_xlabel('Nota promedio', fontsize=9)
        ax2.legend(fontsize=8, loc='lower right', framealpha=0.5)
    else:
        ax2.text(0.5, 0.5, 'Sin datos de materias', ha='center', va='center',
                 transform=ax2.transAxes, fontsize=11, color='#9CA3AF')

    ax2.set_title('Comparativa por materia: tú vs el salón', fontsize=11, fontweight='bold', color=COLOR_EST, pad=10)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    fig2.tight_layout()
    img2_bytes = _fig_a_bytes(fig2)

    # ────────────────────────────────────────────────
    # GRÁFICA 3 — Radar / barras de mejores y peores materias
    # ────────────────────────────────────────────────
    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(6.5, 3), facecolor=BG_FIG)
    for ax in (ax3a, ax3b):
        ax.set_facecolor(BG_FIG)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    if mejores:
        nombres_m = [m[0][:14] + '…' if len(m[0]) > 14 else m[0] for m in mejores]
        vals_m    = [m[1] for m in mejores]
        bars = ax3a.bar(nombres_m, vals_m, color='#10B981', alpha=0.85, zorder=3)
        for bar in bars:
            ax3a.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
                      f'{bar.get_height()}', ha='center', fontsize=9, fontweight='bold', color='#10B981')
        ax3a.set_ylim(0, 11)
        ax3a.set_title('🏆 Mejores materias', fontsize=10, fontweight='bold', color='#10B981')
        ax3a.grid(axis='y', alpha=0.3, linestyle='--')
        ax3a.tick_params(axis='x', labelsize=8)
    else:
        ax3a.text(0.5, 0.5, 'Sin datos', ha='center', va='center',
                  transform=ax3a.transAxes, fontsize=10, color='#9CA3AF')
        ax3a.set_title('🏆 Mejores materias', fontsize=10, color='#10B981')

    if a_mejorar:
        nombres_r = [m[0][:14] + '…' if len(m[0]) > 14 else m[0] for m in a_mejorar]
        vals_r    = [m[1] for m in a_mejorar]
        bars = ax3b.bar(nombres_r, vals_r, color='#EF4444', alpha=0.85, zorder=3)
        for bar in bars:
            ax3b.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
                      f'{bar.get_height()}', ha='center', fontsize=9, fontweight='bold', color='#EF4444')
        ax3b.set_ylim(0, 11)
        ax3b.set_title('📈 A mejorar', fontsize=10, fontweight='bold', color='#EF4444')
        ax3b.grid(axis='y', alpha=0.3, linestyle='--')
        ax3b.tick_params(axis='x', labelsize=8)
    else:
        ax3b.text(0.5, 0.5, '¡Sin materias\na mejorar!', ha='center', va='center',
                  transform=ax3b.transAxes, fontsize=10, color='#10B981')
        ax3b.set_title('📈 A mejorar', fontsize=10, color='#EF4444')

    fig3.tight_layout()
    img3_bytes = _fig_a_bytes(fig3)

    # ────────────────────────────────────────────────
    # CONSTRUCCIÓN DEL PDF
    # ────────────────────────────────────────────────
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
    )

    story = []
    W = letter[0] - 3.6*cm  # ancho útil

    def img_from_bytes(data, width):
        return Image(io.BytesIO(data), width=width, height=width * 0.48)

    def img_tall_from_bytes(data, width, ratio):
        return Image(io.BytesIO(data), width=width, height=width * ratio)

    # ── PÁGINA 1: Portada + tabla de notas ──

    # Encabezado
    story.append(Paragraph('INSTITUCIÓN EDUCATIVA AULATEC', s_titulo))
    story.append(Paragraph('Reporte Académico de Notas', s_subtitulo))
    story.append(Paragraph(f'Año Lectivo {anio}', s_subtitulo))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width='100%', thickness=2, color=PURPLE))
    story.append(Spacer(1, 10))

    # Datos del estudiante
    datos_est = [
        ['Estudiante:', nombre_est, 'Documento:', doc_est],
        ['Grado:', grado_est,       'Promedio general:', str(promedio_general)],
    ]
    t_datos = Table(datos_est, colWidths=[W*0.18, W*0.32, W*0.18, W*0.32])
    t_datos.setStyle(TableStyle([
        ('FONTNAME',  (0,0), (-1,-1), 'Helvetica'),
        ('FONTNAME',  (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',  (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE',  (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (0,-1), PURPLE),
        ('TEXTCOLOR', (2,0), (2,-1), PURPLE),
        ('BACKGROUND',(0,0), (-1,-1), PURPLE_PALE),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [PURPLE_PALE, WHITE]),
        ('GRID',      (0,0), (-1,-1), 0.5, GRAY),
        ('TOPPADDING',(0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',(0,0),(-1,-1), 8),
    ]))
    story.append(t_datos)
    story.append(Spacer(1, 14))

    # Promedios por periodo — mini tabla visual
    story.append(Paragraph('Promedios por Periodo', s_seccion))

    def color_nota(n):
        if n is None: return GRAY
        if n >= 7:    return SUCCESS
        if n >= 6:    return WARNING
        return DANGER

    periodos_data = [['', 'Primer\nPeriodo', 'Segundo\nPeriodo', 'Tercer\nPeriodo', 'Cuarto\nPeriodo']]
    fila_vals = ['Promedio']
    for p in range(1, 5):
        v = promedios_periodo.get(p)
        fila_vals.append(str(v) if v else '—')
    periodos_data.append(fila_vals)

    t_periodos = Table(periodos_data, colWidths=[W*0.2, W*0.2, W*0.2, W*0.2, W*0.2])
    periodo_styles = [
        ('FONTNAME',     (0,0), (-1,-1), 'Helvetica'),
        ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTNAME',     (0,1), (0,1),   'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 9),
        ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND',   (0,0), (-1,0),  PURPLE),
        ('TEXTCOLOR',    (0,0), (-1,0),  WHITE),
        ('BACKGROUND',   (0,1), (0,1),   PURPLE_PALE),
        ('TEXTCOLOR',    (0,1), (0,1),   PURPLE),
        ('GRID',         (0,0), (-1,-1), 0.5, GRAY),
        ('TOPPADDING',   (0,0), (-1,-1), 7),
        ('BOTTOMPADDING',(0,0), (-1,-1), 7),
        ('ROWHEIGHT',    (0,0), (-1,-1), 28),
    ]
    for p in range(1, 5):
        v = promedios_periodo.get(p)
        col = p
        bg_color = colors.HexColor('#D1FAE5') if v and v >= 7 else \
                   colors.HexColor('#FEF3C7') if v and v >= 6 else \
                   colors.HexColor('#FEE2E2') if v else GRAY_LIGHT
        periodo_styles.append(('BACKGROUND', (col,1), (col,1), bg_color))

    t_periodos.setStyle(TableStyle(periodo_styles))
    story.append(t_periodos)
    story.append(Spacer(1, 14))

    # Tabla detalle de calificaciones por periodo
    story.append(Paragraph('Detalle de Calificaciones', s_seccion))

    for periodo_num in range(1, 5):
        cals_periodo = [c for c in calificaciones if c.Periodo == periodo_num]
        if not cals_periodo:
            continue

        avg_p = promedios_periodo.get(periodo_num)
        titulo_periodo = f"{periodos_nombres[periodo_num]}  —  Promedio: {avg_p if avg_p else '—'}"
        story.append(Paragraph(titulo_periodo, estilo(f'p{periodo_num}',
            fontSize=9, fontName='Helvetica-Bold',
            textColor=WHITE,
            backColor=PURPLE_LIGHT,
            leftIndent=4, rightIndent=4,
            spaceBefore=6, spaceAfter=2,
            borderPad=4,
        )))

        filas = [['Materia', 'Actividad', 'Docente', 'Nota', 'Observaciones']]
        for c in cals_periodo:
            docente_nombre = ''
            if c.IdDocente:
                docente_nombre = f"{c.IdDocente.IdUsuario.Nombres} {c.IdDocente.IdUsuario.Apellidos}"
            filas.append([
                c.IdMateria.NombreMateria,
                c.NombreActividad,
                docente_nombre,
                str(c.Nota),
                c.Observaciones or '—',
            ])

        t_cals = Table(filas, colWidths=[W*0.22, W*0.22, W*0.22, W*0.08, W*0.26])
        cal_styles = [
            ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
            ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE',     (0,0), (-1,-1), 8),
            ('ALIGN',        (3,0), (3,-1),  'CENTER'),
            ('BACKGROUND',   (0,0), (-1,0),  PURPLE_PALE),
            ('TEXTCOLOR',    (0,0), (-1,0),  PURPLE),
            ('ROWBACKGROUNDS',(0,1),(-1,-1), [WHITE, GRAY_LIGHT]),
            ('GRID',         (0,0), (-1,-1), 0.4, GRAY),
            ('TOPPADDING',   (0,0), (-1,-1), 4),
            ('BOTTOMPADDING',(0,0), (-1,-1), 4),
            ('LEFTPADDING',  (0,0), (-1,-1), 6),
        ]
        for i, c in enumerate(cals_periodo, start=1):
            nota_val = float(c.Nota)
            bg = colors.HexColor('#D1FAE5') if nota_val >= 7 else \
                 colors.HexColor('#FEF3C7') if nota_val >= 6 else \
                 colors.HexColor('#FEE2E2')
            cal_styles.append(('BACKGROUND', (3, i), (3, i), bg))
        t_cals.setStyle(TableStyle(cal_styles))
        story.append(t_cals)
        story.append(Spacer(1, 6))

    # ── PÁGINA 2: Gráficas ──
    story.append(PageBreak())

    story.append(Paragraph('Análisis Visual del Rendimiento', s_titulo))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=2, color=PURPLE))
    story.append(Spacer(1, 12))

    story.append(Paragraph('Evolución por Periodo', s_seccion))
    story.append(img_from_bytes(img1_bytes, W))
    story.append(Spacer(1, 16))

    story.append(Paragraph('Comparativa por Materia: Tú vs el Salón', s_seccion))
    ratio2 = max(3, len(materias_graf) * 0.55 + 1) / 6.5
    story.append(img_tall_from_bytes(img2_bytes, W, ratio2))
    story.append(Spacer(1, 16))

    # ── PÁGINA 3: Mejores / a mejorar + pie de página ──
    story.append(PageBreak())

    story.append(Paragraph('Fortalezas y Áreas de Mejora', s_titulo))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=2, color=PURPLE))
    story.append(Spacer(1, 12))

    story.append(img_from_bytes(img3_bytes, W))
    story.append(Spacer(1, 20))

    # Tabla resumen mejores / a mejorar
    if mejores or a_mejorar:
        resumen_data = [['🏆 Mejores materias', 'Promedio', '📈 Materias a mejorar', 'Promedio']]
        max_rows = max(len(mejores), len(a_mejorar), 1)
        for i in range(max_rows):
            m_nombre = mejores[i][0]   if i < len(mejores)   else ''
            m_val    = str(mejores[i][1]) if i < len(mejores) else ''
            r_nombre = a_mejorar[i][0]   if i < len(a_mejorar) else ''
            r_val    = str(a_mejorar[i][1]) if i < len(a_mejorar) else ''
            resumen_data.append([m_nombre, m_val, r_nombre, r_val])

        t_resumen = Table(resumen_data, colWidths=[W*0.38, W*0.12, W*0.38, W*0.12])
        t_resumen.setStyle(TableStyle([
            ('FONTNAME',  (0,0), (-1,0),  'Helvetica-Bold'),
            ('FONTNAME',  (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE',  (0,0), (-1,-1), 9),
            ('BACKGROUND',(0,0), (1,0),   colors.HexColor('#D1FAE5')),
            ('BACKGROUND',(2,0), (3,0),   colors.HexColor('#FEE2E2')),
            ('TEXTCOLOR', (0,0), (1,0),   SUCCESS),
            ('TEXTCOLOR', (2,0), (3,0),   DANGER),
            ('ROWBACKGROUNDS',(0,1),(-1,-1), [WHITE, GRAY_LIGHT]),
            ('ALIGN',     (1,0), (1,-1),  'CENTER'),
            ('ALIGN',     (3,0), (3,-1),  'CENTER'),
            ('GRID',      (0,0), (-1,-1), 0.4, GRAY),
            ('TOPPADDING',(0,0), (-1,-1), 5),
            ('BOTTOMPADDING',(0,0),(-1,-1), 5),
            ('LEFTPADDING',(0,0),(-1,-1), 8),
        ]))
        story.append(t_resumen)

    story.append(Spacer(1, 20))

    # Pie de página informativo
    from datetime import datetime
    fecha_gen = datetime.now().strftime('%d/%m/%Y a las %H:%M')
    story.append(HRFlowable(width='100%', thickness=1, color=GRAY))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f'Reporte generado el {fecha_gen} · Institución Educativa AulaTec · Uso académico interno',
        estilo('pie', fontSize=7, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    return buffer.getvalue()
