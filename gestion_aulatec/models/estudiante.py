from django.db import models
from .grado import Grado
from .usuario import Usuario

class Estudiante(models.Model):
    IdEstudiante = models.AutoField(primary_key=True)
    # Clave Foránea a Usuario
    # on_delete=models.CASCADE significa que si el Usuario asociado es eliminado,
    # este Estudiante también será eliminado.
    IdUsuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, unique=True)
    IdGrado = models.ForeignKey(Grado, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        nombre_usuario = f"{self.IdUsuario.Nombres} {self.IdUsuario.Apellidos}" if self.IdUsuario else "Usuario Desconocido"
        grado_info = f" (Grado {self.IdGrado.NumCurso}{self.IdGrado.NumGrado})" if self.IdGrado else ""
        return f"{nombre_usuario}{grado_info}"

    class Meta:
        db_table = 'Estudiante'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
