from django.db import models

class TipoIdentificacion(models.Model):
    IdTipoId = models.AutoField(primary_key=True)
    NombreTipo = models.CharField(max_length=100, verbose_name="Nombre del Documento")
    Abreviatura = models.CharField(max_length=10, unique=True) # Ej: CC, TI, CE

    def __str__(self):
        return self.Abreviatura

    class Meta:
        db_table = 'TipoIdentificacion'
        verbose_name = 'Tipo de Identificación'
        verbose_name_plural = 'Tipos de Identificación'