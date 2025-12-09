from django import forms
from gestion_aulatec.models import Docente

#formulario para el modelo Docente
class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        exclude = ['IdDocente'] #IdDocente es PK autoincremental
        
        labels = {
            'IdUsuario':'Usuario Asociado (Docente)',        
        }
    