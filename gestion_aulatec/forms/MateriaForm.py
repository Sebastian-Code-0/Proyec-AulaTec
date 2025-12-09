from django import forms
from gestion_aulatec.models import Materia

#formulario para el modelo Materia
class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        exclude = ['IdMateria']

        labels = {
            'NombreMateria' : 'Nombre de la Materia',
            'IdDocente' : 'Docente Asignado (Docente)',
        }
