from django.db import models

class Rol(models.Model):
    IdRol = models.AutoField(primary_key=True)
    NombreRol = models.CharField(max_length=50, unique=True) # Ej: Administrador, Docente, Estudiante

    def __str__(self):
        return self.NombreRol

    class Meta:
        db_table = 'Rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'