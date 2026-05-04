from django import forms
from gestion_aulatec.models import Estudiante, Usuario

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = ['IdEstudiante']
        labels = {
            'IdUsuario': 'Usuario Asociado',
            'IdGrado': 'Grado Asignado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['IdUsuario'].queryset = Usuario.objects.filter(
            Rol='Estudiante'
        ).order_by('Nombres', 'Apellidos')
        self.fields['IdUsuario'].label_from_instance = lambda obj: f"{obj.Nombres} {obj.Apellidos} — {obj.NumId}"
        self.fields['IdUsuario'].widget.attrs.update({'size': '1'})
