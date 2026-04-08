from django import forms
from django.core.validators import RegexValidator

from gestion_aulatec.models import Usuario


TIPO_ID_CHOICES = [
    ('', '— Seleccionar —'),
    ('CC', 'CC — Cédula de Ciudadanía'),
    ('T.I.', 'T.I. — Tarjeta de Identidad'),
    ('CE', 'CE — Cédula de Extranjería'),
    ('Pasaporte', 'Pasaporte'),
    ('PPT', 'PPT — Permiso de Protección Temporal'),
    ('NIT', 'NIT — Número de Identificación Tributaria'),
]

ROL_CHOICES = [
    ('', '— Seleccionar —'),
    ('Administrador', 'Administrador'),
    ('Docente', 'Docente'),
    ('Estudiante', 'Estudiante'),
]

_solo_letras = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$',
    message='Solo se permiten letras y espacios, sin números ni símbolos.'
)

_solo_digitos = RegexValidator(
    regex=r'^\d+$',
    message='Solo se permiten dígitos del 0 al 9, sin negativos ni símbolos.'
)


class UsuarioForm(forms.ModelForm):
    TipoId = forms.ChoiceField(
        choices=TIPO_ID_CHOICES,
        label='Tipo de Documento',
    )
    NumId = forms.CharField(
        max_length=10,
        label='Número de Documento',
        validators=[_solo_digitos],
        widget=forms.TextInput(attrs={'placeholder': 'Máximo 10 dígitos'}),
    )
    Nombres = forms.CharField(
        max_length=100,
        label='Nombres',
        validators=[_solo_letras],
        widget=forms.TextInput(attrs={'placeholder': 'Solo letras y espacios'}),
    )
    Apellidos = forms.CharField(
        max_length=100,
        label='Apellidos',
        validators=[_solo_letras],
        widget=forms.TextInput(attrs={'placeholder': 'Solo letras y espacios'}),
    )
    Email = forms.EmailField(
        max_length=100,
        required=True,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'example@example.com'}),
    )
    Rol = forms.ChoiceField(
        choices=ROL_CHOICES,
        label='Rol',
    )
    Celular = forms.CharField(
        max_length=10,
        required=False,
        label='Celular (opcional)',
        validators=[_solo_digitos],
        widget=forms.TextInput(attrs={'placeholder': 'Máximo 10 dígitos'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        label='Contraseña',
        required=True,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña'}),
        label='Confirmar Contraseña',
        required=True,
    )

    class Meta:
        model = Usuario
        fields = ['TipoId', 'NumId', 'Nombres', 'Apellidos', 'Rol', 'Celular']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Al editar un usuario existente las contraseñas no son obligatorias
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False
            self.fields['password'].help_text = 'Deja en blanco para mantener la contraseña actual.'
            self.fields['password_confirm'].help_text = 'Deja en blanco para mantener la contraseña actual.'

    # --- Validaciones de campo ---

    def clean_TipoId(self):
        value = self.cleaned_data.get('TipoId', '').strip()
        if not value:
            raise forms.ValidationError('Debes seleccionar un tipo de documento.')
        return value

    def clean_NumId(self):
        value = self.cleaned_data.get('NumId', '').strip()
        if not (1 <= len(value) <= 10):
            raise forms.ValidationError('El número de documento debe tener entre 1 y 10 dígitos.')
        return value

    def clean_Nombres(self):
        value = self.cleaned_data.get('Nombres', '').strip()
        if not value:
            raise forms.ValidationError('Este campo es obligatorio.')
        return value

    def clean_Apellidos(self):
        value = self.cleaned_data.get('Apellidos', '').strip()
        if not value:
            raise forms.ValidationError('Este campo es obligatorio.')
        return value

    def clean_Rol(self):
        value = self.cleaned_data.get('Rol', '').strip()
        if not value:
            raise forms.ValidationError('Debes seleccionar un rol.')
        return value

    def clean_Celular(self):
        value = self.cleaned_data.get('Celular', '').strip()
        if value and not (1 <= len(value) <= 10):
            raise forms.ValidationError('El celular debe tener entre 1 y 10 dígitos.')
        # Guardar None en la BD cuando está vacío
        return value if value else None

    # --- Validación cruzada de contraseñas ---

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Solo validar coincidencia si al menos una fue ingresada
        if password or password_confirm:
            if password != password_confirm:
                self.add_error('password_confirm', 'Las contraseñas no coinciden.')
        return cleaned_data
