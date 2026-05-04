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

        grado = cleaned_data.get('grado')
        dia = cleaned_data.get('dia_semana')
        docente = cleaned_data.get('docente')

        if grado and dia and hora_inicio and hora_fin:
            qs = Horario.objects.filter(
                grado=grado,
                dia_semana=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    f'Ya existe un horario para {grado} el día {dia} '
                    f'de {hora_inicio.strftime("%H:%M")} a {hora_fin.strftime("%H:%M")}.'
                )

        # Un docente no puede tener dos clases en horarios que se traslapen el mismo día
        if docente and dia and hora_inicio and hora_fin:
            conflicto = Horario.objects.filter(
                docente=docente,
                dia_semana=dia,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            )
            if self.instance.pk:
                conflicto = conflicto.exclude(pk=self.instance.pk)
            if conflicto.exists():
                h = conflicto.first()
                raise forms.ValidationError(
                    f'El docente {docente} ya tiene clase el {dia} '
                    f'de {h.hora_inicio.strftime("%H:%M")} a {h.hora_fin.strftime("%H:%M")} '
                    f'({h.grado} — {h.materia}). No puede dictar dos clases al mismo tiempo.'
                )

        return cleaned_data