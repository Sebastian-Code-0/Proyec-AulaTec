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
    FechaNacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    LugarNacimiento = models.CharField(max_length=100, null=True, blank=True, verbose_name="Lugar de Nacimiento")
    BarrioVereda = models.CharField(max_length=100, null=True, blank=True, verbose_name="Barrio/Vereda de Residencia")
    EPSSeguroMedico = models.CharField(max_length=100, null=True, blank=True, verbose_name="EPS o Seguro Médico")
    TieneCondicionMedica = models.BooleanField(default=False, verbose_name="¿Tiene alguna condición médica?")
    EspecificacionCondicionMedica = models.TextField(blank=True, null=True, verbose_name="Especificar condición médica")
    def __str__(self):
        nombre_usuario = f"{self.IdUsuario.Nombres} {self.IdUsuario.Apellidos}" if self.IdUsuario else "Usuario Desconocido"
        grado_info = f" (Grado {self.IdGrado.NumCurso}{self.IdGrado.NumGrado})" if self.IdGrado else ""
        return f"{nombre_usuario}{grado_info}"

    class Meta:
        db_table = 'Estudiante'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
