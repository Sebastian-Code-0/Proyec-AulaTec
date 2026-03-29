from django import forms
from gestion_aulatec.models import Calificacion

class CalificacionForm(forms.ModelForm):

    class Meta:
        model = Calificacion
        exclude = ['IdCalificacion', 'FechaRegistro', 'FechaActualizacion', 'AnioLectivo']
        labels = {
            'IdEstudiante': 'Estudiante',
            'IdMateria': 'Materia',
            'IdDocente': 'Docente',
            'Periodo': 'Periodo',
            'NombreActividad': 'Nombre de la Actividad',
            'Nota': 'Nota (0.00 - 10.00)',
            'Observaciones': 'Observaciones',
        }
        widgets = {
            'Observaciones': forms.Textarea(attrs={'rows': 3}),
            'Nota': forms.NumberInput(attrs={'min': '0', 'max': '10', 'step': '0.01'}),
        }

    def clean_Nota(self):
        nota = self.cleaned_data.get('Nota')
        if nota is not None:
            if nota < 0 or nota > 10:
                raise forms.ValidationError('La nota debe estar entre 0.00 y 10.00.')
        return nota