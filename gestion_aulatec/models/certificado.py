from django.db import models
from gestion_aulatec.models.estudiante import Estudiante
from gestion_aulatec.models.usuario import Usuario
import uuid
from datetime import datetime, timedelta


class Certificado(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de Aprobación'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('vencido', 'Vencido'),
    ]
    
    TIPO_CHOICES = [
        ('estudio', 'Certificado de Estudio'),
        ('notas', 'Certificado de Notas'),
        ('conducta', 'Certificado de Conducta'),
    ]
    
    IdCertificado = models.AutoField(primary_key=True)
    IdEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='certificados')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='estudio')
    
    # Información de la institución
    nombre_institucion = models.CharField(max_length=200, default='INSTITUCIÓN EDUCATIVA AULATEC')
    nit_institucion = models.CharField(max_length=20, default='900.123.456-7')
    resolucion = models.CharField(
        max_length=500, 
        default='Resolución No. 001234 del 15 de marzo de 2020 - Secretaría de Educación'
    )
    
    # Estado y fechas
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    
    # Usuario que aprueba (administrador)
    aprobado_por = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='certificados_aprobados'
    )
    
    # Código único del certificado
    codigo = models.CharField(max_length=50, unique=True, editable=False)
    
    # Archivo PDF generado
    archivo_pdf = models.CharField(max_length=255, null=True, blank=True)
    
    # Observaciones
    observaciones = models.TextField(null=True, blank=True)
    motivo_rechazo = models.TextField(null=True, blank=True)
    
    # Información adicional del estudiante al momento de emisión
    nombre_completo_estudiante = models.CharField(max_length=200, blank=True)
    documento_estudiante = models.CharField(max_length=20, blank=True)
    grado_estudiante = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'certificados'
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['-fecha_solicitud']
    
    def save(self, *args, **kwargs):
        # Generar código único si no existe
        if not self.codigo:
            self.codigo = self.generar_codigo()
        
        # Guardar información del estudiante al momento de la solicitud
        if not self.nombre_completo_estudiante:
            self.nombre_completo_estudiante = f"{self.IdEstudiante.IdUsuario.Nombres} {self.IdEstudiante.IdUsuario.Apellidos}"
            self.documento_estudiante = self.IdEstudiante.IdUsuario.NumId
            if self.IdEstudiante.IdGrado:
                self.grado_estudiante = f"{self.IdEstudiante.IdGrado.NumGrado}{self.IdEstudiante.IdGrado.NumCurso}"
        
        # Establecer fecha de vencimiento (30 días después de la aprobación)
        if self.estado == 'aprobado' and self.fecha_aprobacion and not self.fecha_vencimiento:
            self.fecha_vencimiento = self.fecha_aprobacion + timedelta(days=30)
        
        super().save(*args, **kwargs)
    
    def generar_codigo(self):
        """Genera un código único para el certificado"""
        año = datetime.now().year
        uuid_corto = str(uuid.uuid4())[:8].upper()
        return f"CERT-{año}-{uuid_corto}"
    
    def esta_vigente(self):
        """Verifica si el certificado está vigente"""
        if self.estado != 'aprobado':
            return False
        if self.fecha_vencimiento:
            return datetime.now() <= self.fecha_vencimiento
        return True
    
    def dias_para_vencer(self):
        """Retorna los días restantes de vigencia"""
        if self.fecha_vencimiento and self.esta_vigente():
            delta = self.fecha_vencimiento - datetime.now()
            return delta.days
        return 0
    
    def __str__(self):
        return f"Certificado {self.codigo} - {self.nombre_completo_estudiante} - {self.get_estado_display()}"