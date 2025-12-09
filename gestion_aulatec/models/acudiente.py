from django.db import models


class Acudiente(models.Model):
    AcudienteId = models.AutoField(primary_key=True)
    TipoId = models.CharField(max_length=50, verbose_name='Tipo Id')
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