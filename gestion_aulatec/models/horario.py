from django.db import models
from .materia import Materia
from .docente import Docente
from .grado import Grado

class Horario(models.Model):
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miércoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sábado', 'Sábado'),
    ]
    
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='horarios')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='horarios')
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aula = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'horarios'
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        ordering = ['dia_semana', 'hora_inicio']
        unique_together = ['grado', 'dia_semana', 'hora_inicio', 'hora_fin']
    
    def __str__(self):
        return f"{self.grado} - {self.materia} - {self.dia_semana} {self.hora_inicio}"
    
    def duracion(self):
        """Calcula la duración de la clase en minutos"""
        from datetime import datetime, timedelta
        inicio = datetime.combine(datetime.today(), self.hora_inicio)
        fin = datetime.combine(datetime.today(), self.hora_fin)
        diferencia = fin - inicio
        return int(diferencia.total_seconds() / 60)