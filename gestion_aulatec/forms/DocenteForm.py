from django import forms
from gestion_aulatec.models import Docente, Usuario

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        exclude = ['IdDocente']
        labels = {
            'IdUsuario': 'Usuario Asociado (Docente)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['IdUsuario'].queryset = Usuario.objects.filter(
            Rol='Docente'
        ).order_by('Nombres', 'Apellidos')
        self.fields['IdUsuario'].label_from_instance = lambda obj: f"{obj.Nombres} {obj.Apellidos} — {obj.NumId}"
        self.fields['IdUsuario'].widget.attrs.update({'size': '1'})