from django.db import models
from .grado import Grado
from .usuario import Usuario

class Estudiante(models.Model):
    IdEstudiante = models.AutoField(primary_key=True)
    IdUsuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, unique=True)
    IdGrado = models.ForeignKey(Grado, on_delete=models.SET_NULL, null=True, blank=True)
    ultima_descarga_notas = models.DateTimeField(null=True, blank=True, verbose_name='Última descarga de reporte de notas')

    def __str__(self):
        nombre_usuario = f"{self.IdUsuario.Nombres} {self.IdUsuario.Apellidos}" if self.IdUsuario else "Usuario Desconocido"
        grado_info = f" (Grado {self.IdGrado.NumGrado}{self.IdGrado.NumCurso})" if self.IdGrado else ""
        return f"{nombre_usuario}{grado_info}"

    class Meta:
        db_table = 'Estudiante'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
