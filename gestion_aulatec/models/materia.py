from django.db import models
from .docente import Docente

class Materia(models.Model):
    IdMateria = models.AutoField(primary_key=True, unique=True)
    NombreMateria = models.CharField(max_length=50, unique=True)
    IdDocente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.IdDocente and self.IdDocente.IdUsuario:
            return f"{self.NombreMateria} (Docente: {self.IdDocente.IdUsuario.Nombres} {self.IdDocente.IdUsuario.Apellidos})"
        return f"{self.NombreMateria} (Docente no asignado)"

    class Meta:
        db_table = 'Materia'
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
