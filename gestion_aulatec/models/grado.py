from django.db import models

class Grado(models.Model):

    IdGrado = models.AutoField(primary_key=True)
    NumGrado = models.IntegerField(unique=True) #El numero de grado debe ser unico 
    NumCurso = models.CharField(max_length=20) # puede ser a, b o 501, 502
    NumEstudiantes = models.IntegerField(default=0) #Campo numerico para la cantidad de estudiantes (default=0) establece un valor inicial

    def __str__(self):
        if self.NumCurso:
            return f"Grado {self.NumGrado} Curso {self.NumCurso}"
        return f"Grado {self.NumGrado}"

    class Meta:
        db_table = 'Grado'
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'
        
        #Esta es una restricción a nivel de base de datos, lo que asegura que no puedas tener dos registros iguales
        unique_together = ('NumGrado','NumCurso') 
