from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView
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
        messages.error(self.request, 'No tienes permiso para acceder a la gestión de usuarios.')
        return redirect('gestion_aulatec:home') # O la página de login
    
# Crear (Agregar un nuevo usuario)
class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_aulatec/usuario_form.html'
    success_url = reverse_lazy('gestion_aulatec:usuario_list') # Redirige al login después de crear

    def form_valid(self, form):
        usuario = form.save(commit=False)
        # Usa el campo 'password' del formulario para hashear
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        messages.success(self.request, 'Usuario registrado con éxito. Ya puedes iniciar sesión.')
        return super().form_valid(form) # Llama al método original para manejar la redirección, etc.
    
    def form_invalid(self, form):
        print("Errores del formulario:", form.errors)   
        return super().form_invalid(form)

# Actualizar (Editar un usuario existente)
class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_aulatec/usuario_form.html'
    success_url = reverse_lazy('gestion_aulatec:usuario_list')  # Redirige a la lista de usuarios después de actualizar uno

# Eliminar (Borrar un usuario)
class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'gestion_aulatec/usuario_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:usuario_list')  # Redirige a la lista de usuarios después de eliminar uno
    
    # Opcional: Personalizar el objeto que se mostrará en el template
    context_object_name = 'usuario' # Para que en el template puedas usar {{ usuario.Nombres }}

#oragnizamos el proyecto