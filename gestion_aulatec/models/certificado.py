from django.db import models
from gestion_aulatec.models.estudiante import Estudiante
from gestion_aulatec.models.materia import Materia
from gestion_aulatec.models.usuario import Usuario


class Certificado(models.Model):
    IdCertificado = models.AutoField(primary_key=True)
    IdEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    IdMateria = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True)
    IdUsuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=50)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=50, unique=True)
    archivo = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=20, default='activo')
    nit_institucion = models.CharField(max_length=20, default='900.123.456-7')  # ← AGREGAR ESTE


    class Meta:
        db_table = "certificados"

    def __str__(self):
        return f"Certificado {self.codigo} - {self.IdEstudiante}"
