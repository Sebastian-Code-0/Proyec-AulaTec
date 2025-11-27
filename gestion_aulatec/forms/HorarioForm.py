from django import forms
from gestion_aulatec.models.horario import Horario
from gestion_aulatec.models.materia import Materia
from gestion_aulatec.models.docente import Docente
from gestion_aulatec.models.grado import Grado

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['grado', 'materia', 'docente', 'dia_semana', 'hora_inicio', 'hora_fin', 'aula']
        widgets = {
            'grado': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'materia': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'docente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'dia_semana': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'hora_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'aula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Aula 101, Laboratorio A'
            }),
        }
        labels = {
            'grado': 'Grado',
            'materia': 'Materia',
            'docente': 'Docente',
            'dia_semana': 'Día de la Semana',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Fin',
            'aula': 'Aula',
        }
    
    # ELIMINA COMPLETAMENTE ESTA FUNCIÓN O COMÉNTALA
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['grado'].queryset = Grado.objects.filter(activo=True)
    #     self.fields['materia'].queryset = Materia.objects.filter(activo=True)
    #     self.fields['docente'].queryset = Docente.objects.filter(activo=True)
    
    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        
        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                raise forms.ValidationError('La hora de fin debe ser mayor a la hora de inicio.')
        
        return cleaned_data