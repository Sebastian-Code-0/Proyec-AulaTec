from django.db import models
from .usuario import Usuario

class Docente(models.Model):
    IdDocente = models.AutoField(primary_key=True)
    # Clave Foránea a Usuario
    # on_delete=models.CASCADE: si el Usuario asociado es eliminado,
    # este Docente también será eliminado.
    # unique=True asegura que cada Usuario solo puede ser un Docente.
    IdUsuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        if self.IdUsuario:
            return f"Docente: {self.IdUsuario.Nombres} {self.IdUsuario.Apellidos}"
        return "Docente sin Usuario asignado"

    class Meta:
        db_table = 'Docente'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
