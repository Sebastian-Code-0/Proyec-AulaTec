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

    def clean(self):
        cleaned_data = super().clean()
        estudiante = cleaned_data.get('IdEstudiante')
        materia = cleaned_data.get('IdMateria')
        periodo = cleaned_data.get('Periodo')
        actividad = cleaned_data.get('NombreActividad')

        if all([estudiante, materia, periodo, actividad]):
            from datetime import date
            anio = date.today().year
            qs = Calificacion.objects.filter(
                IdEstudiante=estudiante,
                IdMateria=materia,
                AnioLectivo=anio,
                Periodo=periodo,
                NombreActividad=actividad,
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    f'Ya existe una calificación para "{actividad}" '
                    f'en el Periodo {periodo} del año {anio}.'
                )
        return cleaned_data