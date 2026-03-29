from django.db import models
from .estudiante import Estudiante
from .materia import Materia
from .docente import Docente

class Calificacion(models.Model):

    PERIODOS = [
        (1, 'Primer Periodo'),
        (2, 'Segundo Periodo'),
        (3, 'Tercer Periodo'),
        (4, 'Cuarto Periodo'),
    ]

    IdCalificacion = models.AutoField(primary_key=True)
    IdEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    IdMateria = models.ForeignKey(Materia, on_delete=models.CASCADE, verbose_name='Materia')
    IdDocente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Docente')
    AnioLectivo = models.IntegerField(verbose_name='Año Lectivo')
    Periodo = models.IntegerField(choices=PERIODOS, verbose_name='Periodo')
    NombreActividad = models.CharField(max_length=100, verbose_name='Nombre de la Actividad')
    Nota = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Nota')
    Observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    FechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    FechaActualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')

    def __str__(self):
        return f"{self.IdEstudiante} | {self.IdMateria} | P{self.Periodo} | {self.NombreActividad}: {self.Nota}"

    class Meta:
        db_table = 'Calificacion'
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        ordering = ['AnioLectivo', 'Periodo', 'IdEstudiante']
        unique_together = ('IdEstudiante', 'IdMateria', 'AnioLectivo', 'Periodo', 'NombreActividad')