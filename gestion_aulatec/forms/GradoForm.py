from django import forms
from gestion_aulatec.models import Grado

class GradoForm(forms.ModelForm):
      class Meta:
            model = Grado
            exclude = ['IdGrado','NumEstudiantes']

            labels = {
                  'NumGrado':'Número de Grado',
                  'NumCurso':'Número de Curso',
            }

            widgets = {
                  'NumCurso': forms.TextInput(attrs={'placeholder': 'A,B,C'})
            }

      def clean(self):
            cleaned_data = super().clean()
            num_grado = cleaned_data.get('NumGrado')
            num_curso = cleaned_data.get('NumCurso')

            if num_grado is not None and num_curso:
                  qs = Grado.objects.filter(NumGrado=num_grado, NumCurso=num_curso)
                  if self.instance.pk:
                        qs = qs.exclude(pk=self.instance.pk)
                  if qs.exists():
                        raise forms.ValidationError(
                              f'Ya existe el Grado {num_grado} con Curso "{num_curso}". '
                              'Elige un número de grado o curso diferente.'
                        )
            return cleaned_data

