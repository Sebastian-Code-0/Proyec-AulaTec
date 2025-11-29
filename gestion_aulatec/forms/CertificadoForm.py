from django import forms
from gestion_aulatec.models.certificado import Certificado

class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = [
            'IdEstudiante',
            'IdMateria',
            'IdUsuario',
            'tipo',
            'codigo',
            'archivo',
            'estado',
        ]
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
