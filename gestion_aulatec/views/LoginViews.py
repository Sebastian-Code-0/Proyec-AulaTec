from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout #funciones de autenticación
from django.contrib.auth.decorators import login_required # Decorador para proteger vistas
from django.contrib import messages # Para mensajes de feedback al usuario
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Mixins para CBVs(Class Based Views)
from django.views.generic import ListView

from gestion_aulatec.models import Usuario,Docente,Estudiante
from gestion_aulatec.forms import LoginForm

#Vistas de Autenticación(Login)
def login_view(request):
    if request.user.is_authenticated: #Si el usuario ya esta logueado, redirigir.
        return redirect('gestion_aulatec:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            NumId = form.cleaned_data['NumId']
            password = form.cleaned_data['password']
            # Autenticar al usuario
            user = authenticate(request,username=NumId, password=password)
            if user is not None:
                login(request, user) #Iniciar Sesión del usuario
                messages.success(request, f'Bienvenido!')
                #redireccionamiento depende del rol
                if user.Rol == 'Administrador':
                    return redirect('gestion_aulatec:admin_dashboard')#una url para el menu de administradores
                elif user.Rol == 'Docente':
                    return redirect('gestion_aulatec:docente_dashboard')#una Url para el menu de docente
                elif user.Rol == 'Estudiante':
                    return redirect('gestion_aulatec:estudiante_dashboard')#una Url para el menu del estudiante
                else: 
                    return redirect('gestion_aulatec:home')#una Url por defecto
            else:
                messages.error(request, 'Numero de identificacion o contraseña incorrecta.')

    else :
        form = LoginForm()
    return render(request, 'gestion_aulatec/login.html', {'form': form })

@login_required #Decorador para asegurar que el usuario este logueado para acceder a las vistas.
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('gestion_aulatec:logout')#Redirigir a la pagina de login despues de cerrar sesion

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/admin_dashboard.html'
    model = Usuario # O el modelo principa que quieras mostrar
    context_object_name = 'usuarios'

    def test_func(self):
        #solo permite el acceso si el usuario es Admninistrador
        return self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:    
            messages.error(self.request, 'No tienes permiso para acceder a esta página.')
            return redirect('gestion_aulatec:home') # Redirige a una página de inicio o login
        return super().handle_no_permission()
    
class DocenteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/docente_dashboard.html'
    model = Docente 
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Docente'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')

class EstudianteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/estudiante_dashboard.html'
    model = Estudiante # Ejemplo: un estudiante ve su perfil
    context_object_name = 'estudiante_perfil' # Asegúrate de filtrar por el usuario logueado en get_queryset

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Estudiante'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')

    def get_queryset(self):
        # Filtra para obtener el perfil del estudiante logueado
        return Estudiante.objects.filter(IdUsuario=self.request.user)

def home_view(request):
    return render(request,'gestion_aulatec/home.html')
