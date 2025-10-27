from django.db import models
from .tipoIdentificacion import TipoIdentificacion # Asume que lo importas

class Acudiente(models.Model):
    AcudienteId = models.AutoField(primary_key=True)
    
    # NORMALIZACIÓN: Ahora es una FK a la tabla TipoIdentificacion
    IdTipoId = models.ForeignKey(TipoIdentificacion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo Id')
    
    # Eliminamos el campo TipoId de texto y usamos IdTipoId
    NumId = models.CharField(max_length=50, unique=True)
    Nombres = models.CharField(max_length=100)
    Apellidos = models.CharField(max_length=100)
    Celular = models.CharField(max_length=20)
    Parentesco = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.Nombres} {self.Apellidos}"
    
    class Meta:
        db_table = 'Acudiente'
        verbose_name = 'Acudiente'
        verbose_name_plural = 'Acudientes'