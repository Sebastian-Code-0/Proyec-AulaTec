from django import forms
from gestion_aulatec.models import Estudiante

# formulario para el modelo Estudiante
class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = ['IdEstudiante'] # IdEstudiante es PK autoincremental
        # O:
        # fields = ['IdUsuario', 'IdGrado']
        labels = {
            'IdUsuario': 'Usuario Asociado',
            'IdGrado': 'Grado Asignado',
        }
