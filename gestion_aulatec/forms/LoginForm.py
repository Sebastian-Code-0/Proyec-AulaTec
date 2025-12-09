from django import forms

#formulario del login 
class LoginForm(forms.Form):
    NumId = forms.CharField(max_length=50, label='Número de identificación')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
