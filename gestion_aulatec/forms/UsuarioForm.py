from django import forms
# IMPORTANTE: Asegúrate de que estos modelos estén accesibles
# (ya sea que estén definidos en un models.py central o en archivos separados)
from gestion_aulatec.models import Usuario, Rol, TipoIdentificacion 


# Formulario para el modelo Usuario
class UsuarioForm(forms.ModelForm):
    """
    Formulario para la creación de usuarios que incluye campos para
    la contraseña y su confirmación.
    """
    # Campos de contraseña y confirmación fuera del modelo
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label='Contraseña',
        required=True # La contraseña debe ser obligatoria al crear un usuario
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, 
        label='Confirmar Contraseña',
        required=True
    )

    class Meta:
        model = Usuario
        # CORRECCIÓN CRÍTICA: Se usan las Claves Foráneas (FK) normalizadas
        # IdTipoId y IdRol en lugar de los antiguos campos de texto (TipoId y Rol).
        fields = [
            'IdTipoId',     # <-- Nueva FK a TipoIdentificacion
            'NumId', 
            'Nombres', 
            'Apellidos', 
            'IdRol',        # <-- Nueva FK a Rol
            'Celular'
        ]

    def clean(self):
        """
        Realiza validación personalizada, incluyendo la coincidencia de contraseñas.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # La validación se ejecuta solo si ambas contraseñas están presentes
        if password and password_confirm:
            if password != password_confirm:
                # Agregamos un error al campo de confirmación
                self.add_error('password_confirm', "Las contraseñas no coinciden.") 
        
        return cleaned_data