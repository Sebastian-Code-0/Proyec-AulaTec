from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from gestion_aulatec.models import Usuario, Docente, Estudiante
from gestion_aulatec.forms import LoginForm

# Vistas de Autenticación(Login)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('gestion_aulatec:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            NumId = form.cleaned_data['NumId']
            password = form.cleaned_data['password']
            # Autenticar al usuario
            user = authenticate(request, username=NumId, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido!')
                # Redireccionamiento depende del rol
                if user.Rol == 'Administrador':
                    return redirect('gestion_aulatec:admin_dashboard')
                elif user.Rol == 'Docente':
                    return redirect('gestion_aulatec:docente_dashboard')
                elif user.Rol == 'Estudiante':
                    return redirect('gestion_aulatec:estudiante_dashboard')
                else: 
                    return redirect('gestion_aulatec:home')
            else:
                messages.error(request, 'Número de identificación o contraseña incorrecta.')
    else:
        form = LoginForm()
    
    return render(request, 'gestion_aulatec/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('gestion_aulatec:login')  # ← CORREGIDO


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/admin_dashboard.html'
    model = Usuario
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:    
            messages.error(self.request, 'No tienes permiso para acceder a esta página.')
            return redirect('gestion_aulatec:home')
        return super().handle_no_permission()


class DocenteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/docente_dashboard.html'
    model = Docente
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Docente'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('gestion_aulatec:home')  # ← CORREGIDO


class EstudianteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/estudiante_dashboard.html'
    model = Estudiante
    context_object_name = 'estudiante_perfil'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Estudiante'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('gestion_aulatec:home')  # ← CORREGIDO

    def get_queryset(self):
        return Estudiante.objects.filter(IdUsuario=self.request.user)


def home_view(request):
    return render(request, 'gestion_aulatec/home.html')