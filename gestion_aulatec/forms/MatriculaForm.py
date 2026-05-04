from datetime import date
from django import forms
from django.core.validators import RegexValidator
from gestion_aulatec.models import Matricula, Grado

# --- Validators ---
_solo_letras = RegexValidator(
    r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s\-]+$',
    'Solo se permiten letras, espacios y guiones.'
)
_solo_numeros = RegexValidator(
    r'^\d{1,10}$',
    'Solo se permiten dígitos, máximo 10.'
)

# --- Choices ---
TIPO_DOC_ESTUDIANTE = [
    ('', '— Seleccione —'),
    ('TI', 'Tarjeta de Identidad (TI)'),
    ('RC', 'Registro Civil (RC)'),
    ('CC', 'Cédula de Ciudadanía (CC)'),
    ('CE', 'Cédula de Extranjería (CE)'),
    ('PA', 'Pasaporte (PA)'),
    ('PEP', 'Permiso Especial de Permanencia (PEP)'),
]

TIPO_DOC_ACUDIENTE = [
    ('', '— Seleccione —'),
    ('CC', 'Cédula de Ciudadanía (CC)'),
    ('CE', 'Cédula de Extranjería (CE)'),
    ('PA', 'Pasaporte (PA)'),
    ('NIT', 'NIT'),
    ('PEP', 'Permiso Especial de Permanencia (PEP)'),
]

GRADOS_CHOICES = [
    ('', '— Seleccione —'),
    ('Preescolar', 'Preescolar'),
    ('1°', 'Primero (1°)'),
    ('2°', 'Segundo (2°)'),
    ('3°', 'Tercero (3°)'),
    ('4°', 'Cuarto (4°)'),
    ('5°', 'Quinto (5°)'),
    ('6°', 'Sexto (6°)'),
    ('7°', 'Séptimo (7°)'),
    ('8°', 'Octavo (8°)'),
    ('9°', 'Noveno (9°)'),
    ('10°', 'Décimo (10°)'),
    ('11°', 'Once (11°)'),
]

# "Ciudad (Departamento)" — permite buscar por ciudad O por departamento
MUNICIPIOS_COLOMBIA = [
    'Bogotá D.C. (Bogotá D.C.)',
    # Antioquia
    'Medellín (Antioquia)', 'Bello (Antioquia)', 'Itagüí (Antioquia)',
    'Envigado (Antioquia)', 'Apartadó (Antioquia)', 'Rionegro (Antioquia)',
    'Turbo (Antioquia)', 'Sabaneta (Antioquia)', 'La Estrella (Antioquia)',
    'Copacabana (Antioquia)', 'Girardota (Antioquia)', 'Barbosa (Antioquia)',
    'Caldas (Antioquia)', 'Caucasia (Antioquia)', 'Chigorodó (Antioquia)',
    'El Carmen de Viboral (Antioquia)', 'Marinilla (Antioquia)', 'Yarumal (Antioquia)',
    'Andes (Antioquia)', 'Jericó (Antioquia)', 'Santa Fe de Antioquia (Antioquia)',
    # Valle del Cauca
    'Cali (Valle del Cauca)', 'Buenaventura (Valle del Cauca)', 'Palmira (Valle del Cauca)',
    'Tuluá (Valle del Cauca)', 'Cartago (Valle del Cauca)', 'Buga (Valle del Cauca)',
    'Yumbo (Valle del Cauca)', 'Jamundí (Valle del Cauca)', 'Candelaria (Valle del Cauca)',
    'Florida (Valle del Cauca)', 'Pradera (Valle del Cauca)', 'El Cerrito (Valle del Cauca)',
    'Dagua (Valle del Cauca)', 'Sevilla (Valle del Cauca)', 'Zarzal (Valle del Cauca)',
    'Roldanillo (Valle del Cauca)', 'La Unión (Valle del Cauca)',
    # Atlántico
    'Barranquilla (Atlántico)', 'Soledad (Atlántico)', 'Malambo (Atlántico)',
    'Sabanalarga (Atlántico)', 'Baranoa (Atlántico)', 'Galapa (Atlántico)',
    'Puerto Colombia (Atlántico)',
    # Bolívar
    'Cartagena (Bolívar)', 'Magangué (Bolívar)', 'El Carmen de Bolívar (Bolívar)',
    'Mompox (Bolívar)', 'Turbaco (Bolívar)', 'Arjona (Bolívar)', 'Simití (Bolívar)',
    # Cundinamarca
    'Soacha (Cundinamarca)', 'Zipaquirá (Cundinamarca)', 'Facatativá (Cundinamarca)',
    'Chía (Cundinamarca)', 'Fusagasugá (Cundinamarca)', 'Madrid (Cundinamarca)',
    'Mosquera (Cundinamarca)', 'Funza (Cundinamarca)', 'Girardot (Cundinamarca)',
    'La Mesa (Cundinamarca)', 'Cajicá (Cundinamarca)', 'Tocancipá (Cundinamarca)',
    'Sopó (Cundinamarca)', 'Cota (Cundinamarca)', 'Tenjo (Cundinamarca)',
    'Villeta (Cundinamarca)', 'Ubaté (Cundinamarca)', 'Sibaté (Cundinamarca)',
    # Santander
    'Bucaramanga (Santander)', 'Floridablanca (Santander)', 'Girón (Santander)',
    'Piedecuesta (Santander)', 'Barrancabermeja (Santander)', 'San Gil (Santander)',
    'Socorro (Santander)', 'Vélez (Santander)', 'Málaga (Santander)',
    # Norte de Santander
    'Cúcuta (Norte de Santander)', 'Ocaña (Norte de Santander)',
    'Pamplona (Norte de Santander)', 'Villa del Rosario (Norte de Santander)',
    'Los Patios (Norte de Santander)', 'El Zulia (Norte de Santander)',
    # Caldas
    'Manizales (Caldas)', 'La Dorada (Caldas)', 'Villamaría (Caldas)',
    'Chinchiná (Caldas)', 'Riosucio (Caldas)', 'Salamina (Caldas)',
    # Risaralda
    'Pereira (Risaralda)', 'Dosquebradas (Risaralda)', 'Santa Rosa de Cabal (Risaralda)',
    'La Virginia (Risaralda)', 'Marsella (Risaralda)', 'Belén de Umbría (Risaralda)',
    # Quindío
    'Armenia (Quindío)', 'Calarcá (Quindío)', 'La Tebaida (Quindío)',
    'Montenegro (Quindío)', 'Quimbaya (Quindío)', 'Circasia (Quindío)',
    # Tolima
    'Ibagué (Tolima)', 'Espinal (Tolima)', 'Melgar (Tolima)',
    'Honda (Tolima)', 'Chaparral (Tolima)', 'Líbano (Tolima)', 'Mariquita (Tolima)',
    # Meta
    'Villavicencio (Meta)', 'Acacías (Meta)', 'Granada (Meta)',
    'Puerto López (Meta)', 'Cumaral (Meta)', 'Restrepo (Meta)',
    # Huila
    'Neiva (Huila)', 'Pitalito (Huila)', 'Garzón (Huila)',
    'La Plata (Huila)', 'Campoalegre (Huila)', 'Palermo (Huila)',
    # Magdalena
    'Santa Marta (Magdalena)', 'El Banco (Magdalena)', 'Ciénaga (Magdalena)',
    'Fundación (Magdalena)', 'Plato (Magdalena)', 'Aracataca (Magdalena)',
    # Cesar
    'Valledupar (Cesar)', 'Aguachica (Cesar)', 'La Paz (Cesar)',
    'Codazzi (Cesar)', 'Bosconia (Cesar)', 'Curumaní (Cesar)',
    # La Guajira
    'Riohacha (La Guajira)', 'Maicao (La Guajira)', 'Uribia (La Guajira)',
    'San Juan del Cesar (La Guajira)', 'Manaure (La Guajira)',
    # Córdoba
    'Montería (Córdoba)', 'Lorica (Córdoba)', 'Cereté (Córdoba)',
    'Sahagún (Córdoba)', 'Tierralta (Córdoba)', 'Montelíbano (Córdoba)',
    'Planeta Rica (Córdoba)',
    # Sucre
    'Sincelejo (Sucre)', 'Corozal (Sucre)', 'Sampués (Sucre)',
    'San Marcos (Sucre)', 'Tolú (Sucre)',
    # Cauca
    'Popayán (Cauca)', 'Santander de Quilichao (Cauca)', 'El Tambo (Cauca)',
    'Puerto Tejada (Cauca)', 'Patía (Cauca)', 'Miranda (Cauca)',
    # Nariño
    'Pasto (Nariño)', 'Tumaco (Nariño)', 'Ipiales (Nariño)',
    'La Unión (Nariño)', 'Túquerres (Nariño)', 'Samaniego (Nariño)',
    # Boyacá
    'Tunja (Boyacá)', 'Sogamoso (Boyacá)', 'Duitama (Boyacá)',
    'Chiquinquirá (Boyacá)', 'Paipa (Boyacá)', 'Moniquirá (Boyacá)',
    'Puerto Boyacá (Boyacá)',
    # Chocó
    'Quibdó (Chocó)', 'Istmina (Chocó)', 'Riosucio (Chocó)', 'Tadó (Chocó)',
    # Caquetá
    'Florencia (Caquetá)', 'San Vicente del Caguán (Caquetá)',
    'Belén de los Andaquíes (Caquetá)',
    # Putumayo
    'Mocoa (Putumayo)', 'Puerto Asís (Putumayo)', 'Orito (Putumayo)',
    'Valle del Guamuez (Putumayo)',
    # Casanare
    'Yopal (Casanare)', 'Aguazul (Casanare)', 'Villanueva (Casanare)',
    'Tauramena (Casanare)',
    # Arauca
    'Arauca (Arauca)', 'Saravena (Arauca)', 'Arauquita (Arauca)', 'Tame (Arauca)',
    # Vichada
    'Puerto Carreño (Vichada)', 'La Primavera (Vichada)',
    # Guainía
    'Inírida (Guainía)',
    # Vaupés
    'Mitú (Vaupés)',
    # Amazonas
    'Leticia (Amazonas)', 'Puerto Nariño (Amazonas)',
    # San Andrés y Providencia
    'San Andrés (San Andrés y Providencia)', 'Providencia (San Andrés y Providencia)',
    # Guaviare
    'San José del Guaviare (Guaviare)', 'El Retorno (Guaviare)',
]

EPS_COLOMBIA = [
    # Contributivo
    'Sura (Contributivo)',
    'Compensar (Contributivo)',
    'Nueva EPS (Contributivo)',
    'Sanitas (Contributivo)',
    'Salud Total (Contributivo)',
    'Famisanar (Contributivo)',
    'Medimás (Contributivo)',
    'Coomeva (Contributivo)',
    'Comfenalco Valle (Contributivo)',
    'Convida - Comfenalco Antioquia (Contributivo)',
    'SOS - Comfamiliar Nariño (Contributivo)',
    # Medicina prepagada / Pólizas
    'Colmédica (Medicina prepagada)',
    'Colsanitas (Medicina prepagada)',
    'Seguros Bolívar Salud (Póliza)',
    'Suramericana Salud (Póliza)',
    'Seguros Sura (Póliza)',
    # Subsidiado
    'Coosalud (Subsidiado)',
    'Mutual Ser (Subsidiado)',
    'Capital Salud (Subsidiado)',
    'Emssanar (Subsidiado)',
    'Asmet Salud (Subsidiado)',
    'Pijaos Salud (Subsidiado)',
    'Capresoca (Subsidiado)',
    'Comparta (Subsidiado)',
    'Dusakawi (Subsidiado)',
    'Anaswayuu (Subsidiado)',
    'Mallamas (Subsidiado)',
    'Savia Salud (Subsidiado)',
    'Ecoopsos (Subsidiado)',
    # Sin afiliación
    'SISBEN (Vinculado)',
    'Póliza privada',
    'No tiene EPS',
    'Otra',
]


class MatriculaForm(forms.ModelForm):

    # ---- Estudiante ----
    EstudianteNombres = forms.CharField(
        max_length=100, label='Nombres del Estudiante',
        validators=[_solo_letras],
        widget=forms.TextInput(attrs={'placeholder': 'Ej: María Fernanda'}),
    )
    EstudianteApellidos = forms.CharField(
        max_length=100, label='Apellidos del Estudiante',
        validators=[_solo_letras],
        widget=forms.TextInput(attrs={'placeholder': 'Ej: García López'}),
    )
    EstudianteEmail = forms.EmailField(
        label='Correo Electrónico del Estudiante',
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
    )
    EstudianteTipoId = forms.ChoiceField(
        choices=TIPO_DOC_ESTUDIANTE, label='Tipo de Documento',
    )
    EstudianteNumId = forms.CharField(
        max_length=10, label='Número de Documento',
        widget=forms.TextInput(attrs={'placeholder': 'Máx. 10 dígitos', 'maxlength': '10', 'inputmode': 'numeric'}),
    )
    EstudianteCelular = forms.CharField(
        max_length=10, label='Teléfono del Estudiante', required=False,
        widget=forms.TextInput(attrs={'placeholder': '10 dígitos', 'maxlength': '10', 'inputmode': 'numeric'}),
    )

    # ---- Acudiente ----
    AcudienteTipoId = forms.ChoiceField(
        choices=TIPO_DOC_ACUDIENTE, label='Tipo de Identificación Acudiente',
    )
    AcudienteNumId = forms.CharField(
        max_length=10, label='Número de Identificación Acudiente',
        widget=forms.TextInput(attrs={'placeholder': 'Máx. 10 dígitos', 'maxlength': '10', 'inputmode': 'numeric'}),
    )
    AcudienteNombres = forms.CharField(
        max_length=100, label='Nombres del Acudiente',
        validators=[_solo_letras],
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Carlos Alberto'}),
    )
    AcudienteApellidos = forms.CharField(
        max_length=100, label='Apellidos del Acudiente',
        validators=[_solo_letras],
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Martínez Ruiz'}),
    )
    AcudienteCelular = forms.CharField(
        max_length=10, label='Celular del Acudiente',
        widget=forms.TextInput(attrs={'placeholder': '10 dígitos', 'maxlength': '10', 'inputmode': 'numeric'}),
    )
    AcudienteParentesco = forms.CharField(
        max_length=50, label='Parentesco con el Estudiante',
        validators=[_solo_letras],
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Madre, Padre, Tío'}),
    )

    # ---- Condición médica: override BooleanField → Si/No radio ----
    TieneCondicionMedica = forms.TypedChoiceField(
        choices=[('1', 'Sí'), ('0', 'No')],
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect(attrs={'class': 'si-no-radio'}),
        label='¿Tiene alguna condición médica?',
        initial='0',
    )

    # ---- Último grado: override CharField → select ----
    UltimoGradoCursado = forms.ChoiceField(
        choices=GRADOS_CHOICES, label='Último Grado Cursado',
    )

    class Meta:
        model = Matricula
        fields = [
            'IdGrado', 'AnioLectivo', 'NombreColegio',
            'FechaNacimientoEstudiante', 'LugarNacimientoEstudiante',
            'BarrioVeredaEstudiante', 'EPSSeguroMedicoEstudiante',
            'TieneCondicionMedica', 'EspecificacionCondicionMedica',
            'UltimoGradoCursado', 'InstitucionAnterior',
            'CiudadMunicipioInstitucionAnterior',
            'RepiteGrado', 'RequiereApoyoPedagogico', 'AutorizaTratamientoDatos',
            'DocIdentidadEstudiantePresentado', 'CertificadoNotasAnteriorPresentado',
            'FotocopiaCarnetVacunacionPresentado', 'FotocopiaEpsSeguroMedicoPresentado',
            'FotosTamanoDocumentoPresentadas', 'CertificadoMedicoPresentado',
            'CopiaCedulaAcudientePresentado', 'ComprobanteResidenciaAcudientePresentado',
        ]
        widgets = {
            'FechaNacimientoEstudiante': forms.DateInput(attrs={'type': 'date'}),
            'EspecificacionCondicionMedica': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describa la condición médica...',
                'id': 'id_EspecificacionCondicionMedica',
            }),
            'LugarNacimientoEstudiante': forms.TextInput(attrs={
                'list': 'municipios_list',
                'autocomplete': 'off',
                'placeholder': 'Escriba ciudad o departamento...',
            }),
            'EPSSeguroMedicoEstudiante': forms.TextInput(attrs={
                'list': 'eps_list',
                'autocomplete': 'off',
                'placeholder': 'Escriba el nombre de la EPS...',
            }),
            'CiudadMunicipioInstitucionAnterior': forms.TextInput(attrs={
                'list': 'municipios_list',
                'autocomplete': 'off',
                'placeholder': 'Escriba ciudad o departamento...',
            }),
            'BarrioVeredaEstudiante': forms.TextInput(attrs={'placeholder': 'Ej: La Floresta'}),
            'NombreColegio': forms.TextInput(attrs={'placeholder': 'Nombre del colegio anterior'}),
            'InstitucionAnterior': forms.TextInput(attrs={'placeholder': 'Nombre de la institución anterior'}),
            'AnioLectivo': forms.NumberInput(attrs={'placeholder': '2025', 'min': '2000', 'max': '2100'}),
        }

    # ---- Validaciones individuales ----
    def clean_EstudianteNumId(self):
        v = self.cleaned_data.get('EstudianteNumId', '').strip()
        if not v.isdigit():
            raise forms.ValidationError('Solo se permiten números.')
        if len(v) > 10:
            raise forms.ValidationError('Máximo 10 dígitos.')
        return v

    def clean_AcudienteNumId(self):
        v = self.cleaned_data.get('AcudienteNumId', '').strip()
        if not v.isdigit():
            raise forms.ValidationError('Solo se permiten números.')
        if len(v) > 10:
            raise forms.ValidationError('Máximo 10 dígitos.')
        return v

    def clean_EstudianteCelular(self):
        v = self.cleaned_data.get('EstudianteCelular', '').strip()
        if v and not v.isdigit():
            raise forms.ValidationError('Solo se permiten números.')
        return v

    def clean_AcudienteCelular(self):
        v = self.cleaned_data.get('AcudienteCelular', '').strip()
        if v and not v.isdigit():
            raise forms.ValidationError('Solo se permiten números.')
        return v

    def clean_EstudianteTipoId(self):
        v = self.cleaned_data.get('EstudianteTipoId', '')
        if not v:
            raise forms.ValidationError('Seleccione un tipo de documento.')
        return v

    def clean_AcudienteTipoId(self):
        v = self.cleaned_data.get('AcudienteTipoId', '')
        if not v:
            raise forms.ValidationError('Seleccione un tipo de documento.')
        return v

    def clean_UltimoGradoCursado(self):
        v = self.cleaned_data.get('UltimoGradoCursado', '')
        if not v:
            raise forms.ValidationError('Seleccione el último grado cursado.')
        return v

    def clean(self):
        cleaned_data = super().clean()
        tiene = cleaned_data.get('TieneCondicionMedica')
        especificacion = cleaned_data.get('EspecificacionCondicionMedica', '').strip()
        if tiene and not especificacion:
            self.add_error('EspecificacionCondicionMedica', 'Debe especificar la condición médica.')
        if not tiene:
            cleaned_data['EspecificacionCondicionMedica'] = ''
        autoriza = cleaned_data.get('AutorizaTratamientoDatos')
        if not autoriza:
            self.add_error('AutorizaTratamientoDatos', 'La autorización de tratamiento de datos es obligatoria para completar la matrícula.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['IdGrado'].queryset = Grado.objects.all()
        self.fields['IdGrado'].label_from_instance = lambda obj: str(obj)
        self.fields['IdGrado'].empty_label = '— Seleccione grado —'
        # Pre-llenar AnioLectivo con el año actual solo si es un formulario vacío (sin datos previos)
        if not args and not kwargs.get('instance'):
            self.fields['AnioLectivo'].initial = date.today().year
