from django.shortcuts import render, redirect
<<<<<<< HEAD
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.utils import timezone
from datetime import timedelta
from gestion_aulatec.models.certificado import Certificado
from gestion_aulatec.models import Usuario, Docente, Estudiante
from gestion_aulatec.forms import LoginForm


# ==================== VISTAS DE AUTENTICACIÓN ====================

def login_view(request):
    """Vista de login - Autentica y redirige según el rol del usuario"""
    if request.user.is_authenticated:
        # Si el usuario ya está logueado, redirigir según su rol
        if request.user.Rol == 'Administrador':
            return redirect('gestion_aulatec:admin_dashboard')
        elif request.user.Rol == 'Docente':
            return redirect('gestion_aulatec:docente_dashboard')
        elif request.user.Rol == 'Estudiante':
            return redirect('gestion_aulatec:estudiante_dashboard')
        else:
            return redirect('gestion_aulatec:home')
    
=======
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
>>>>>>> 4e2f81b62d3d85f4ea86504f7061355e11f3faf0
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            NumId = form.cleaned_data['NumId']
            password = form.cleaned_data['password']
<<<<<<< HEAD
            
            # Autenticar al usuario
            user = authenticate(request, username=NumId, password=password)
            
            if user is not None:
                login(request, user)  # Iniciar sesión del usuario
                messages.success(request, f'¡Bienvenido, {user.Nombres}!')
                
                # Redireccionamiento según el rol
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
    """Vista de logout - Cierra sesión y redirige al login"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('gestion_aulatec:login')  # ← CORREGIDO: antes decía 'logout'


def home_view(request):
    """Vista de la página principal"""
    return render(request, 'gestion_aulatec/home.html')


# ==================== DASHBOARDS ====================

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Dashboard del Administrador
    Muestra estadísticas y gestión de usuarios
    """
    template_name = 'gestion_aulatec/admin_dashboard.html'
    model = Usuario
    context_object_name = 'usuarios'

    def test_func(self):
        """Solo permite acceso a usuarios con rol Administrador"""
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'
    
    def handle_no_permission(self):
        """Maneja cuando el usuario no tiene permisos"""
        if self.request.user.is_authenticated:
            messages.error(self.request, 'No tienes permiso para acceder a esta página.')
            return redirect('gestion_aulatec:home')
        return super().handle_no_permission()
    
    def get_context_data(self, **kwargs):
        """Agrega estadísticas y datos al contexto"""
        context = super().get_context_data(**kwargs)
        
        # Agregar estadísticas de certificados
        try:
            # Total de certificados
            context['total_certificados'] = Certificado.objects.count()
            
            # Certificados de esta semana
            hace_una_semana = timezone.now() - timedelta(days=7)
            context['certificados_semana'] = Certificado.objects.filter(
                fecha_emision__gte=hace_una_semana
            ).count()
            
            # Últimos 5 certificados generados
            context['certificados_recientes'] = Certificado.objects.select_related(
                'IdEstudiante__IdUsuario', 
                'IdMateria'
            ).order_by('-fecha_emision')[:5]
            
        except Exception as e:
            print(f"Error al cargar certificados en admin dashboard: {e}")
            context['total_certificados'] = 0
            context['certificados_semana'] = 0
            context['certificados_recientes'] = []
        
        return context


class DocenteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Dashboard del Docente
    Muestra información relevante para profesores
    """
    template_name = 'gestion_aulatec/docente_dashboard.html'
    model = Docente
    context_object_name = 'docente_perfil'
    
    def test_func(self):
        """Solo permite acceso a usuarios con rol Docente"""
        return self.request.user.is_authenticated and self.request.user.Rol == 'Docente'

    def handle_no_permission(self):
        """Maneja cuando el usuario no tiene permisos"""
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('gestion_aulatec:home')
    
    def get_queryset(self):
        """Filtra para obtener el perfil del docente logueado"""
        return Docente.objects.filter(IdUsuario=self.request.user)


class EstudianteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Dashboard del Estudiante
    Muestra información del estudiante y sus certificados disponibles
    """
    template_name = 'gestion_aulatec/estudiante_dashboard.html'
    model = Estudiante
    context_object_name = 'estudiante_perfil'

    def test_func(self):
        """Solo permite acceso a usuarios con rol Estudiante"""
        return self.request.user.is_authenticated and self.request.user.Rol == 'Estudiante'

    def handle_no_permission(self):
        """Maneja cuando el usuario no tiene permisos"""
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('gestion_aulatec:home')

    def get_queryset(self):
        """Filtra para obtener el perfil del estudiante logueado"""
        return Estudiante.objects.filter(IdUsuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        """Agrega certificados del estudiante al contexto"""
        context = super().get_context_data(**kwargs)
        
        # Agregar certificados del estudiante logueado
        try:
            estudiante = Estudiante.objects.get(IdUsuario=self.request.user)
            
            # Obtener certificados del estudiante
            certificados = Certificado.objects.filter(
                IdEstudiante=estudiante,
                # estado='activo'  # Descomenta para mostrar solo activos
            ).select_related(
                'IdMateria',
                'IdEstudiante__IdUsuario'
            ).order_by('-fecha_emision')
            
            context['certificados'] = certificados
            context['total_certificados'] = certificados.count()
            context['certificados_activos'] = certificados.filter(estado='activo').count()
            
        except Estudiante.DoesNotExist:
            context['certificados'] = []
            context['total_certificados'] = 0
            context['certificados_activos'] = 0
            messages.warning(
                self.request, 
                'Tu perfil de estudiante aún no ha sido creado. Contacta al administrador.'
            )
            
        except Exception as e:
            print(f"Error al cargar certificados del estudiante: {e}")
            context['certificados'] = []
            context['total_certificados'] = 0
            context['certificados_activos'] = 0
            messages.error(
                self.request, 
                'Hubo un problema al cargar tus certificados. Intenta nuevamente más tarde.'
            )
        
        return context
=======
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
>>>>>>> 4e2f81b62d3d85f4ea86504f7061355e11f3faf0
