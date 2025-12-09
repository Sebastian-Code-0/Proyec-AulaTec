from fpdf import FPDF
from datetime import datetime
import os
from django.conf import settings


class CertificadoPDF(FPDF):
    def __init__(self, certificado):
        super().__init__()
        self.certificado = certificado
        
    def header(self):
        """Encabezado del certificado con logo y título"""
        # Logo (puedes crear uno simple o usar una imagen)
        # Si tienes un logo, descomenta esta línea:
        # self.image('ruta/al/logo.png', 10, 8, 30)
        
        # Dibujar un escudo simple (círculo con iniciales)
        self.set_fill_color(41, 128, 185)  # Azul
        self.circle(105, 25, 15, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 16)
        self.text(98, 28, 'ATC')
        
        # Restaurar color de texto
        self.set_text_color(0, 0, 0)
        
        # Título de la institución
        self.set_font('Arial', 'B', 16)
        self.cell(0, 50, '', 0, 1)  # Espacio para el logo
        self.cell(0, 10, self.certificado.nombre_institucion, 0, 1, 'C')
        
        # NIT
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f'NIT: {self.certificado.nit_institucion}', 0, 1, 'C')
        
        # Resolución
        self.set_font('Arial', 'I', 9)
        self.multi_cell(0, 5, self.certificado.resolucion, 0, 'C')
        
        self.ln(10)
    
    def footer(self):
        """Pie de página con información de validez"""
        self.set_y(-30)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        
        # Información de validez
        if self.certificado.fecha_vencimiento:
            texto_validez = f'Este certificado tiene validez de 30 días desde su emisión.'
            self.cell(0, 5, texto_validez, 0, 1, 'C')
            texto_vence = f'Fecha de vencimiento: {self.certificado.fecha_vencimiento.strftime("%d de %B de %Y")}'
            self.cell(0, 5, texto_vence, 0, 1, 'C')
        
        # Código de verificación
        self.set_font('Arial', 'B', 8)
        self.cell(0, 5, f'Código de verificación: {self.certificado.codigo}', 0, 1, 'C')
    
    def generar_contenido(self):
        """Genera el contenido principal del certificado"""
        # Título del certificado
        self.set_font('Arial', 'B', 18)
        self.set_text_color(41, 128, 185)
        self.cell(0, 15, 'CERTIFICADO DE ESTUDIO', 0, 1, 'C')
        self.ln(5)
        
        # Restaurar color
        self.set_text_color(0, 0, 0)
        
        # Número de certificado
        self.set_font('Arial', 'B', 11)
        self.cell(0, 10, f'Certificado No. {self.certificado.codigo}', 0, 1, 'C')
        self.ln(10)
        
        # Cuerpo del certificado
        self.set_font('Arial', '', 12)
        
        # Texto principal
        texto_principal = (
            f'La {self.certificado.nombre_institucion}, identificada con '
            f'NIT {self.certificado.nit_institucion}, hace constar que:'
        )
        self.multi_cell(0, 8, texto_principal, 0, 'J')
        self.ln(8)
        
        # Información del estudiante
        self.set_font('Arial', 'B', 13)
        self.cell(0, 10, self.certificado.nombre_completo_estudiante.upper(), 0, 1, 'C')
        
        self.set_font('Arial', '', 12)
        self.cell(0, 8, f'Identificado(a) con documento No. {self.certificado.documento_estudiante}', 0, 1, 'C')
        self.ln(8)
        
        # Estado de vinculación
        self.set_font('Arial', '', 12)
        texto_vinculacion = (
            f'Se encuentra vinculado(a) a esta institución educativa '
            f'cursando el grado {self.certificado.grado_estudiante}. '
            f'El estudiante se encuentra en estado ACTIVO desde su fecha de matrícula.'
        )
        self.multi_cell(0, 8, texto_vinculacion, 0, 'J')
        self.ln(10)
        
        # Fecha de emisión
        fecha_emision = self.certificado.fecha_aprobacion or datetime.now()
        self.cell(0, 8, f'Fecha de emisión: {fecha_emision.strftime("%d de %B de %Y")}', 0, 1, 'L')
        self.ln(15)
        
        # Firmas
        self.set_font('Arial', 'B', 11)
        
        # Espacio para firmas (dos columnas)
        x_inicial = self.get_x()
        y_firma = self.get_y()
        
        # Firma izquierda (Rector/Director)
        self.set_xy(30, y_firma)
        self.cell(70, 10, '', 'T', 0, 'C')  # Línea de firma
        self.set_xy(30, y_firma + 12)
        self.cell(70, 5, 'RECTOR(A)', 0, 0, 'C')
        self.set_xy(30, y_firma + 17)
        self.set_font('Arial', '', 9)
        self.cell(70, 5, self.certificado.nombre_institucion, 0, 0, 'C')
        
        # Firma derecha (Coordinador/Secretario)
        self.set_font('Arial', 'B', 11)
        self.set_xy(110, y_firma)
        self.cell(70, 10, '', 'T', 0, 'C')  # Línea de firma
        self.set_xy(110, y_firma + 12)
        self.cell(70, 5, 'SECRETARIO(A) ACADÉMICO(A)', 0, 0, 'C')
        
        # Información del aprobador
        if self.certificado.aprobado_por:
            self.set_xy(110, y_firma + 17)
            self.set_font('Arial', '', 9)
            nombre_aprobador = f"{self.certificado.aprobado_por.Nombres} {self.certificado.aprobado_por.Apellidos}"
            self.cell(70, 5, nombre_aprobador, 0, 0, 'C')


def generar_certificado_pdf(certificado):
    """
    Genera el PDF del certificado y lo guarda
    
    Args:
        certificado: Instancia del modelo Certificado
    
    Returns:
        str: Ruta relativa del archivo PDF generado
    """
    # Crear instancia del PDF
    pdf = CertificadoPDF(certificado)
    pdf.add_page()
    pdf.generar_contenido()
    
    # Crear directorio si no existe
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'certificados')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Nombre del archivo
    nombre_archivo = f'certificado_{certificado.codigo}.pdf'
    ruta_completa = os.path.join(pdf_dir, nombre_archivo)
    
    # Guardar PDF
    pdf.output(ruta_completa)
    
    # Retornar ruta relativa
    return f'certificados/{nombre_archivo}'