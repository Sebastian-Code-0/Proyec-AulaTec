from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout #funciones de autenticación
from django.contrib.auth.decorators import login_required # Decorador para proteger vistas
from django.contrib import messages # Para mensajes de feedback al usuario
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Mixins para CBVs(Class Based Views)
from django.views.generic import ListView

from gestion_aulatec.models import Usuario,Docente,Estudiante
from gestion_aulatec.models.matricula import Matricula
from gestion_aulatec.models.grado import Grado
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
                # messages.success(request, f'Bienvenido!')
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

@login_required
def logout_view(request):
    list(messages.get_messages(request))
    logout(request)
    return redirect('gestion_aulatec:login')

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/admin_dashboard.html'
    model = Usuario
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from datetime import date
        from gestion_aulatec.models import Estudiante, Docente, Matricula, Certificado, Materia, Horario

        anio_actual = date.today().year

        context['total_estudiantes'] = Estudiante.objects.count()
        context['total_docentes'] = Docente.objects.count()
        context['total_matriculas_activas'] = Matricula.objects.filter(Activa=True, AnioLectivo=anio_actual).count()
        context['total_materias'] = Materia.objects.count()
        context['total_horarios'] = Horario.objects.filter(activo=True).count()
        context['cert_pendientes'] = Certificado.objects.filter(estado='pendiente').count()
        context['cert_aprobados'] = Certificado.objects.filter(estado='aprobado').count()
        context['anio_actual'] = anio_actual

        return context
    
class DocenteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/docente_dashboard.html'
    model = Docente

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Docente'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')

    def get_queryset(self):
        return Docente.objects.filter(IdUsuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from gestion_aulatec.models import Materia, Horario, Calificacion, Estudiante
        from django.db.models import Avg, Count

        try:
            docente = Docente.objects.get(IdUsuario=self.request.user)

            # Materias del docente
            materias = Materia.objects.filter(IdDocente=docente)

            # Horarios del docente
            horarios = Horario.objects.filter(
                docente=docente, activo=True
            ).select_related('materia', 'grado').order_by('dia_semana', 'hora_inicio')

            # Calificaciones registradas por el docente
            calificaciones = Calificacion.objects.filter(
                IdDocente=docente
            ).select_related('IdEstudiante__IdUsuario', 'IdMateria').order_by('-FechaRegistro')

            # Resumen por materia
            resumen_materias = []
            for materia in materias:
                cals = calificaciones.filter(IdMateria=materia)
                promedio = cals.aggregate(Avg('Nota'))['Nota__avg']
                estudiantes = Estudiante.objects.filter(
                    IdGrado__horarios__materia=materia,
                    IdGrado__horarios__docente=docente
                ).distinct()
                resumen_materias.append({
                    'materia': materia,
                    'total_calificaciones': cals.count(),
                    'promedio': round(promedio, 2) if promedio else None,
                    'total_estudiantes': estudiantes.count(),
                    'estudiantes': estudiantes.select_related('IdUsuario')[:5],
                })

            context['docente'] = docente
            context['materias'] = materias
            context['horarios'] = horarios
            context['calificaciones_recientes'] = calificaciones[:10]
            context['resumen_materias'] = resumen_materias
            context['total_calificaciones'] = calificaciones.count()

        except Docente.DoesNotExist:
            context['docente'] = None

        return context

class EstudianteDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'gestion_aulatec/estudiante_dashboard.html'
    model = Estudiante
    context_object_name = 'estudiante_perfil'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Estudiante'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')

    def get_queryset(self):
        return Estudiante.objects.filter(IdUsuario=self.request.user).select_related('IdUsuario', 'IdGrado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            from django.db.models import Avg
            from gestion_aulatec.models import Calificacion, Horario
            estudiante = Estudiante.objects.get(IdUsuario=self.request.user)

            calificaciones = Calificacion.objects.filter(
                IdEstudiante=estudiante
            ).select_related('IdMateria', 'IdDocente__IdUsuario').order_by('Periodo', 'IdMateria')

            promedios = {}
            for periodo in range(1, 5):
                avg = calificaciones.filter(Periodo=periodo).aggregate(Avg('Nota'))['Nota__avg']
                promedios[periodo] = round(avg, 2) if avg else None

            horario = []
            if estudiante.IdGrado:
                horario = Horario.objects.filter(
                    grado=estudiante.IdGrado,
                    activo=True
                ).select_related('materia', 'docente__IdUsuario').order_by('dia_semana', 'hora_inicio')

            context['estudiante'] = estudiante
            context['calificaciones'] = calificaciones
            context['promedios'] = promedios
            context['horario'] = horario
            context['periodos'] = [
                (1, 'Primer Periodo'),
                (2, 'Segundo Periodo'),
                (3, 'Tercer Periodo'),
                (4, 'Cuarto Periodo'),
            ]
            context['anio_actual'] = date.today().year
        except Estudiante.DoesNotExist:
            context['estudiante'] = None
            context['calificaciones'] = []
            context['promedios'] = {}
            context['horario'] = []
            context['periodos'] = []

        return context
def home_view(request):
    context = {
        'total_estudiantes': Estudiante.objects.count(),
        'total_docentes': Docente.objects.count(),
        'total_matriculas': Matricula.objects.count(),
        'total_grados': Grado.objects.count(),
    }
    return render(request, 'gestion_aulatec/home.html', context)
