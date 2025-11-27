from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Modelo de Usuario personalizado para AulaTec
    """
    ROLES = (
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('administrador', 'Administrador'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    documento = models.CharField(max_length=20, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"


class Curso(models.Model):
    """
    Modelo para los cursos de AulaTec
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    codigo = models.CharField(max_length=20, unique=True)
    profesor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='cursos_impartidos')
    creditos = models.IntegerField(default=0)
    cupo_maximo = models.IntegerField(default=30)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def estudiantes_matriculados(self):
        return self.matriculas.filter(activo=True).count()
    
    @property
    def tiene_cupo(self):
        return self.estudiantes_matriculados < self.cupo_maximo


class Matricula(models.Model):
    """
    Modelo para las matrículas de estudiantes en cursos
    """
    ESTADOS = (
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    )
    
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='matriculas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='matriculas')
    fecha_matricula = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activa')
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        unique_together = ('estudiante', 'curso')
        ordering = ['-fecha_matricula']
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.curso.nombre}"