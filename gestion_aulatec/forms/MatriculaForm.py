from django import forms
# Asegúrate de importar todos los modelos necesarios
from gestion_aulatec.models import (
    Matricula, Grado, Estudiante, Acudiente,
    historialAcademico, ChecklistDocumentos,
)

class MatriculaForm(forms.ModelForm):
    # --- FKs Y DATOS CLAVE (Se definen manualmente si son ModelChoiceField o si son de otra tabla) ---
    
    # FKs (ModelChoiceField) que serán usados para la Matrícula
    IdEstudiante = forms.ModelChoiceField(
        queryset=Estudiante.objects.all(),
        label="Estudiante a Matricular"
    )
    IdGrado = forms.ModelChoiceField(
        queryset=Grado.objects.all(),
        label="Grado a Matricular"
    )
    IdAcudiente = forms.ModelChoiceField(
        queryset=Acudiente.objects.all(),
        label="Acudiente Principal"
    )
    
    # --- CAMPOS DE HISTORIAL ACADÉMICO (Manuales) ---
    # Estos campos se guardarán en la nueva tabla HistorialAcademico
    UltimoGradoCursado = forms.CharField(max_length=50, label="Último Grado Cursado")
    InstitucionAnterior = forms.CharField(max_length=200, label="Institución Educativa Anterior")
    CiudadMunicipioInstitucionAnterior = forms.CharField(max_length=100, label="Ciudad/Municipio Inst. Anterior")
    RepiteGrado = forms.BooleanField(required=False, label="¿Repite Grado?")
    RequiereApoyoPedagogico = forms.BooleanField(required=False, label="¿Requiere Apoyo Pedagógico?")

    # --- CAMPOS DE CHECKLIST DE DOCUMENTOS (Manuales) ---
    # Estos campos se guardarán en la nueva tabla ChecklistDocumentos
    DocIdentidadEstudiantePresentado = forms.BooleanField(required=False, label="Doc. Identidad Presentado")
    CertificadoNotasAnteriorPresentado = forms.BooleanField(required=False, label="Certificado Notas Anterior Presentado")
    FotocopiaCarnetVacunacionPresentado = forms.BooleanField(required=False, label="Fotocopia Carnet Vacunación Presentado")
    FotocopiaEpsSeguroMedicoPresentado = forms.BooleanField(required=False, label="Fotocopia EPS Presentada")
    FotosTamanoDocumentoPresentadas = forms.BooleanField(required=False, label="Fotos Tamaño Documento Presentadas")
    CertificadoMedicoPresentado = forms.BooleanField(required=False, label="Certificado Médico Presentado")
    CopiaCedulaAcudientePresentado = forms.BooleanField(required=False, label="Copia Cédula Acudiente Presentado")
    ComprobanteResidenciaAcudientePresentado = forms.BooleanField(required=False, label="Comprobante Residencia Acudiente Presentado")
    
    #CAMPOS BIOGRÁFICOS DE ESTUDIANTE (Manuales)
    #Estos deben reflejar la estructura de Estudiante que modificamos
    FechaNacimiento = forms.DateField(label="Fecha de Nacimiento del Estudiante", widget=forms.DateInput(attrs={'type': 'date'}))
    LugarNacimiento = forms.CharField(max_length=100, label="Lugar de Nacimiento del Estudiante")
    BarrioVereda = forms.CharField(max_length=100, label="Barrio/Vereda de Residencia")
    EPSSeguroMedico = forms.CharField(max_length=100, label="EPS o Seguro Médico")
    TieneCondicionMedica = forms.BooleanField(required=False, label="¿Tiene alguna condición médica?")
    EspecificacionCondicionMedica = forms.CharField(required=False, widget=forms.Textarea, label="Especificar condición médica")


    class Meta:
        model = Matricula
        # AHORA SOLO INCLUIMOS LOS CAMPOS QUE QUEDARON EN EL MODELO MATRICULA NORMALIZADO
        fields = [
            'NumMatricula',
            'IdEstudiante', 
            'IdGrado',      
            'IdAcudiente',  
            'AnioLectivo',
            'NombreColegio',
            'AutorizaTratamientoDatos',
            'Activa',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Puedes remover estas líneas si ya están definidas arriba como ModelChoiceField
        # self.fields['IdGrado'].queryset = Grado.objects.all() 

    def clean(self):
        return super().clean()