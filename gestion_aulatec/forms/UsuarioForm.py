from django import forms
from gestion_aulatec.models import Usuario

#formulario para el modelo Usuario
class UsuarioForm(forms.ModelForm):
    # Añadimos un campo de contraseña y confirmación que NO están en el modelo
    # Esto es solo para la entrada del formulario
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = Usuario
        # NO INCLUYAS 'password' aquí, porque AbstractBaseUser ya lo maneja internamente.
        # Los campos que se incluyen aquí son los que *tú* definiste en tu modelo.
        fields = ['TipoId', 'NumId', 'Nombres', 'Apellidos', 'Rol', 'Celular']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.") # Error asociado a un campo
            # O raise forms.ValidationError("Las contraseñas no coinciden.") para un error global
        return cleaned_data
