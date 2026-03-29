from django.contrib import admin
from .models.calificacion import Calificacion

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('IdEstudiante', 'IdMateria', 'IdDocente', 'AnioLectivo', 'Periodo', 'NombreActividad', 'Nota')
    list_filter = ('AnioLectivo', 'Periodo', 'IdMateria')
    search_fields = ('IdEstudiante__IdUsuario__Nombres', 'IdEstudiante__IdUsuario__Apellidos', 'NombreActividad')
    ordering = ('AnioLectivo', 'Periodo')
# Register your models here.
