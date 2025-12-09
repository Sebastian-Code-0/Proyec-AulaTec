# gestion_aulatec/forms.py

from django import forms
# Asegúrate de que tu modelo 'Matricula' esté importado
from gestion_aulatec.models import Matricula, Grado

class MatriculaForm(forms.ModelForm):
    # Campos que NO están en el modelo Matricula pero son necesarios para la vista
    # Los datos de estos campos se usarán para crear los objetos Usuario y Acudiente
    EstudianteNombres = forms.CharField(max_length=100, label="Nombres del estudiante")
    EstudianteApellidos = forms.CharField(max_length=100, label="Apellidos del estudiante")
    EstudianteTipoId = forms.CharField(max_length=20, label="Tipo de documento")
    EstudianteNumId = forms.CharField(max_length=50, label="Número de documento")
    EstudianteCelular = forms.CharField(max_length=20, label="Teléfono de contacto del estudiante", required=False)

    AcudienteTipoId = forms.CharField(label="Tipo de Identificación Acudiente", max_length=50) 
    AcudienteNumId = forms.CharField(label="Número de Identificación Acudiente", max_length=50)
    AcudienteNombres = forms.CharField(label="Nombres del Acudiente", max_length=100)
    AcudienteApellidos = forms.CharField(label="Apellidos del Acudiente", max_length=100)
    AcudienteCelular = forms.CharField(label="Celular del Acudiente", max_length=20)
    AcudienteParentesco = forms.CharField(label="Parentesco con el Estudiante", max_length=50)

    class Meta:
        model = Matricula
        # AQUI es donde declaras explícitamente los campos que quieres incluir del modelo
        fields = [
            'IdGrado',
            'AnioLectivo',
            'NombreColegio',
            'FechaNacimientoEstudiante',
            'LugarNacimientoEstudiante',
            'BarrioVeredaEstudiante',
            'EPSSeguroMedicoEstudiante',
            'TieneCondicionMedica',
            'EspecificacionCondicionMedica',
            'UltimoGradoCursado',
            'InstitucionAnterior',
            'CiudadMunicipioInstitucionAnterior',
            'RepiteGrado',
            'RequiereApoyoPedagogico',
            'AutorizaTratamientoDatos',
            'DocIdentidadEstudiantePresentado',
            'CertificadoNotasAnteriorPresentado',
            'FotocopiaCarnetVacunacionPresentado',
            'FotocopiaEpsSeguroMedicoPresentado',
            'FotosTamanoDocumentoPresentadas',
            'CertificadoMedicoPresentado',
            'CopiaCedulaAcudientePresentado',
            'ComprobanteResidenciaAcudientePresentado',
        ]
        widgets = {
            'FechaNacimientoEstudiante': forms.DateInput(attrs={'type': 'date'}),
            # Un 'widget' para el área de texto con más filas
            'EspecificacionCondicionMedica': forms.Textarea(attrs={'rows': 3}), 
        }

    def clean(self):
        # El método clean ahora debe usar los nombres de campo del modelo
        cleaned_data = super().clean()
        if cleaned_data.get('TieneCondicionMedica') and not cleaned_data.get('EspecificacionCondicionMedica'):
            self.add_error('EspecificacionCondicionMedica', 'Debe especificar la condición médica.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['IdGrado'].queryset = Grado.objects.all()