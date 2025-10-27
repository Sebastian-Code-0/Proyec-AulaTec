from django.db import models

class Matricula(models.Model):
    NumMatricula = models.CharField(max_length=100, unique=True, verbose_name="Número de Matrícula")
    
    # --- REFERENCIAS FKs ---
    IdEstudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE, verbose_name="Estudiante")
    IdGrado = models.ForeignKey('Grado', on_delete=models.CASCADE, verbose_name="Grado a Matricular")
    IdAcudiente = models.ForeignKey('Acudiente', on_delete=models.CASCADE, verbose_name="Acudiente")
    
    # --- DATOS PROPIOS DE LA TRANSACCIÓN ---
    AnioLectivo = models.IntegerField(verbose_name="Año Lectivo")
    NombreColegio = models.CharField(max_length=200, verbose_name="Nombre del Colegio de Procedencia")
    Activa = models.BooleanField(default=True, verbose_name="Matrícula Activa")
    FechaMatricula = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Matrícula")
    
    # Autorizaciones (Estas tienen sentido quedar aquí si son específicas de esta transacción/año)
    AutorizaTratamientoDatos = models.BooleanField(default=False, verbose_name="Autoriza Tratamiento de Datos")

    # Los datos de Historial Académico y Checklist se acceden a través de la relación inversa
    # (ej. matricula.historialacademico)
    def __str__(self):
        return f"Matrícula {self.NumMatricula} - {self.IdEstudiante.IdUsuario.Nombres}"
    
    class Meta:
        db_table = 'Matricula'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'

    