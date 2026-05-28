from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView
from django.contrib.auth.views import PasswordChangeView
import random 
import string
from django.contrib import messages

from gestion_aulatec.models import Usuario
from gestion_aulatec.forms import UsuarioForm

# Leer (Listar todos los usuarios)
class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'gestion_aulatec/usuario_list.html'
    context_object_name = 'usuarios' # Nombre de la variable en la plantilla para la lista de usuarios
    def test_func(self):
        # Solo administradores pueden ver la lista de usuarios
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')
    
class UsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_aulatec/usuario_form.html'
    success_url = reverse_lazy('gestion_aulatec:usuario_list') # Redirige al login después de crear

    def form_valid(self, form):
        usuario = form.save(commit=False)
        
        # 1. Capturamos los datos directamente del cleaned_data (Más seguro)
        password_plana = form.cleaned_data.get('password')
        correo_destino = form.cleaned_data.get('Email') # Verifica si en tu form es 'Email' o 'email'
        
        # 2. Enviamos el correo (usando la variable segura)
        try:
            rol = usuario.Rol if usuario.Rol else 'Usuario'
            asunto = f"Bienvenido a AulaTec - Credenciales de {rol}"
            mensaje = f"""
            Hola {usuario.Nombres},
            
            Se ha creado tu cuenta de docente en la plataforma AulaTec.
            
            Tus credenciales de acceso son:
            Usuario (Documento): {usuario.NumId}
            Contraseña: {password_plana}
            
            Puedes ingresar aquí: {self.request.build_absolute_uri('/login/')}
            """
            
            from django.core.mail import send_mail
            from django.conf import settings
            
            if correo_destino:
                send_mail(
                    asunto,
                    mensaje,
                    settings.EMAIL_HOST_USER,
                    [correo_destino],
                    fail_silently=False,
                )

        except Exception as e:
            messages.warning(self.request, 'Usuario creado, pero hubo un error con el correo.')

        # 3. Hasheamos y quitamos el cambio obligatorio
        usuario.set_password(password_plana)
        usuario.debe_cambiar_password = False
        usuario.save()

        # Saltar super().form_valid() para evitar doble save
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.success_url)
    def form_invalid(self, form):
        return super().form_invalid(form)

# Actualizar (Editar un usuario existente)
class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_aulatec/usuario_form.html'
    success_url = reverse_lazy('gestion_aulatec:usuario_list')

    def form_valid(self, form):
        usuario = form.save(commit=False)
        nueva_password = form.cleaned_data.get('password')
        if nueva_password:
            usuario.set_password(nueva_password)
        usuario.save()
        messages.success(self.request, 'Usuario actualizado con éxito.')
        return redirect(self.success_url)

# Eliminar (Borrar un usuario)
class UsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')
    model = Usuario
    template_name = 'gestion_aulatec/usuario_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:usuario_list')  # Redirige a la lista de usuarios después de eliminar uno
    
    # Opcional: Personalizar el objeto que se mostrará en el template
    context_object_name = 'usuario' # Para que en el template puedas usar {{ usuario.Nombres }}

class CambiarPasswordView(LoginRequiredMixin, PasswordChangeView):
    # Esta es la plantilla que crearemos en el siguiente paso
    template_name = 'gestion_aulatec/cambiar_password.html' 
    
    def get_success_url(self):
        user = self.request.user
        if user.Rol == 'Administrador':
            return reverse_lazy('gestion_aulatec:admin_dashboard')
        elif user.Rol == 'Docente':
            return reverse_lazy('gestion_aulatec:docente_dashboard')
        else:
            return reverse_lazy('gestion_aulatec:estudiante_dashboard')

    def form_valid(self, form):
        # OBTENEMOS AL USUARIO ACTUAL
        user = self.request.user
        
        # APAGAMOS EL INTERRUPTOR DE CAMBIO OBLIGATORIO
        user.debe_cambiar_password = False
        user.save()
        
        messages.success(self.request, '¡Contraseña actualizada con éxito! Ya puedes navegar.')
        return super().form_valid(form)

