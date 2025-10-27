from django.db import models

class HistorialAcademico(models.Model):
    IdHistorial = models.AutoField(primary_key=True)
    
    # Relación 1 a 1: Cada matrícula tiene un único historial
    IdMatricula = models.OneToOneField('Matricula', on_delete=models.CASCADE, verbose_name="Matrícula Asociada")
    
    UltimoGradoCursado = models.CharField(max_length=50, verbose_name="Último Grado Cursado")
    InstitucionAnterior = models.CharField(max_length=200, verbose_name="Institución Educativa Anterior")
    CiudadMunicipioInstitucionAnterior = models.CharField(max_length=100, verbose_name="Ciudad/Municipio de la Institución Anterior")
    RepiteGrado = models.BooleanField(default=False, verbose_name="¿Repite Grado?")
    RequiereApoyoPedagogico = models.BooleanField(default=False, verbose_name="¿Requiere Apoyo Pedagógico?")
    # ------------------------------------
    
    def __str__(self):
        return f"Historial para Matrícula {self.IdMatricula.NumMatricula}"

    class Meta:
        db_table = 'HistorialAcademico'
        verbose_name = 'Historial Académico'
        verbose_name_plural = 'Historiales Académicos'