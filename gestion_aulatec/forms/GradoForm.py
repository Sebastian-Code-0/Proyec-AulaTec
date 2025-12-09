from django import forms
from gestion_aulatec.models import Grado

#formulario para el modelo Grado
class GradoForm(forms.ModelForm):
      class Meta:
            model = Grado
            exclude = ['IdGrado','NumEstudiantes'] #IdGrado es PK, NumEstudiantes Se Actualiza con logica

            labels = {
                  'NumGrado':'Número de Grado',
                  'NumCurso':'Número de Curso',
            }

            widgets = {
                  'NumCurso': forms.TextInput(attrs={'placeholder': 'A,B,C'})
            }

