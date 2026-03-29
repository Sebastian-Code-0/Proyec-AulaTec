from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Avg

from gestion_aulatec.models import Calificacion, Estudiante, Materia
from gestion_aulatec.forms import CalificacionForm


# --- Mixins de permisos ---

class EsAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('gestion_aulatec:home')


class EsDocenteOAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.Rol in ['Administrador', 'Docente']

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('gestion_aulatec:home')


class EsEstudianteMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.Rol == 'Estudiante'

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('gestion_aulatec:home')


# --- Vistas ---

class CalificacionListView(EsDocenteOAdminMixin, ListView):
    model = Calificacion
    template_name = 'gestion_aulatec/calificacion_list.html'
    context_object_name = 'calificaciones'

    def get_queryset(self):
        user = self.request.user
        if user.Rol == 'Administrador':
            qs = Calificacion.objects.all()
        else:
            qs = Calificacion.objects.filter(IdDocente__IdUsuario=user)

        # Filtros
        estudiante = self.request.GET.get('estudiante')
        grado = self.request.GET.get('grado')
        periodo = self.request.GET.get('periodo')
        materia = self.request.GET.get('materia')

        if estudiante:
            qs = qs.filter(IdEstudiante__pk=estudiante)
        if grado:
            qs = qs.filter(IdEstudiante__IdGrado__pk=grado)
        if periodo:
            qs = qs.filter(Periodo=periodo)
        if materia:
            qs = qs.filter(IdMateria__pk=materia)

        return qs.order_by('AnioLectivo', 'Periodo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from gestion_aulatec.models import Estudiante, Grado, Materia
        import json

        estudiantes = Estudiante.objects.select_related(
            'IdUsuario', 'IdGrado'
        ).order_by('IdUsuario__Nombres')

        materias = Materia.objects.all().order_by('NombreMateria')

        # Datos para el filtro en cascada (JSON para JavaScript)
        estudiantes_json = [
            {
                'pk': str(e.pk),
                'nombre': f"{e.IdUsuario.Nombres} {e.IdUsuario.Apellidos}",
                'grado': str(e.IdGrado.pk) if e.IdGrado else ''
            }
            for e in estudiantes
        ]

        materias_json = [
            {
                'pk': str(m.pk),
                'nombre': m.NombreMateria,
                'grado': str(m.IdDocente.pk) if m.IdDocente else ''
            }
            for m in materias
        ]

        context['estudiantes'] = estudiantes
        context['grados'] = Grado.objects.all().order_by('NumGrado')
        context['materias'] = materias
        context['periodos'] = [
            (1, 'Primer Periodo'),
            (2, 'Segundo Periodo'),
            (3, 'Tercer Periodo'),
            (4, 'Cuarto Periodo'),
        ]
        context['estudiantes_json'] = json.dumps(estudiantes_json)
        context['materias_json'] = json.dumps(materias_json)
        context['filtro_estudiante'] = self.request.GET.get('estudiante', '')
        context['filtro_grado'] = self.request.GET.get('grado', '')
        context['filtro_periodo'] = self.request.GET.get('periodo', '')
        context['filtro_materia'] = self.request.GET.get('materia', '')
        if self.request.user.Rol == 'Administrador':
            context['base_template'] = 'gestion_aulatec/base_admin.html'
        else:
            context['base_template'] = 'gestion_aulatec/base_docente.html'
        return context

class CalificacionEstudianteView(LoginRequiredMixin, ListView):
    """
    Estudiante: ve sus propias calificaciones con promedios por periodo.
    Admin/Docente: pueden ver las calificaciones de cualquier estudiante.
    """
    model = Calificacion
    template_name = 'gestion_aulatec/calificacion_estudiante.html'
    context_object_name = 'calificaciones'

    def get_queryset(self):
        user = self.request.user
        if user.Rol == 'Estudiante':
            estudiante = Estudiante.objects.get(IdUsuario=user)
            return Calificacion.objects.filter(
                IdEstudiante=estudiante
            ).order_by('Periodo', 'IdMateria')
        # Admin o Docente consultando un estudiante específico por pk en la URL
        return Calificacion.objects.filter(
            IdEstudiante__pk=self.kwargs.get('pk')
        ).order_by('Periodo', 'IdMateria')

2
class CalificacionCreateView(EsDocenteOAdminMixin, CreateView):
    model = Calificacion
    form_class = CalificacionForm
    template_name = 'gestion_aulatec/calificacion_form.html'
    success_url = reverse_lazy('gestion_aulatec:calificacion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.Rol == 'Administrador':
            context['base_template'] = 'gestion_aulatec/base_admin.html'
        else:
            context['base_template'] = 'gestion_aulatec/base_docente.html'
        return context

    def get_form(self, form_class=None):
        from gestion_aulatec.models import Docente, Horario, Estudiante
        form = super().get_form(form_class)
        user = self.request.user
        if user.Rol == 'Docente':
            docente = Docente.objects.get(IdUsuario=user)
            form.fields['IdMateria'].queryset = Materia.objects.filter(
                IdDocente=docente
            )
            grados = Horario.objects.filter(
                docente=docente
            ).values_list('grado', flat=True)
            form.fields['IdEstudiante'].queryset = Estudiante.objects.filter(
                IdGrado__in=grados
            ).select_related('IdUsuario')
            form.fields['IdDocente'].queryset = Docente.objects.filter(
                IdUsuario=user
            )
            form.fields['IdDocente'].initial = docente
            form.fields['IdDocente'].widget.attrs['disabled'] = True
        return form

    def form_valid(self, form):
        from datetime import date
        user = self.request.user
        if user.Rol == 'Docente':
            from gestion_aulatec.models import Docente
            form.instance.IdDocente = Docente.objects.get(IdUsuario=user)
        form.instance.AnioLectivo = date.today().year
        messages.success(self.request, 'Calificación registrada correctamente.')
        return super().form_valid(form)


class CalificacionUpdateView(EsDocenteOAdminMixin, UpdateView):
    model = Calificacion
    form_class = CalificacionForm
    template_name = 'gestion_aulatec/calificacion_form.html'
    success_url = reverse_lazy('gestion_aulatec:calificacion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.Rol == 'Administrador':
            context['base_template'] = 'gestion_aulatec/base_admin.html'
        else:
            context['base_template'] = 'gestion_aulatec/base_docente.html'
        return context

    def get_form(self, form_class=None):
        from gestion_aulatec.models import Docente, Horario, Estudiante
        form = super().get_form(form_class)
        user = self.request.user
        if user.Rol == 'Docente':
            docente = Docente.objects.get(IdUsuario=user)
            form.fields['IdMateria'].queryset = Materia.objects.filter(
                IdDocente=docente
            )
            grados = Horario.objects.filter(
                docente=docente
            ).values_list('grado', flat=True)
            form.fields['IdEstudiante'].queryset = Estudiante.objects.filter(
                IdGrado__in=grados
            ).select_related('IdUsuario')
            form.fields['IdDocente'].queryset = Docente.objects.filter(
                IdUsuario=user
            )
            form.fields['IdDocente'].initial = docente
            form.fields['IdDocente'].widget.attrs['disabled'] = True
        return form

    def form_valid(self, form):
        from datetime import date
        user = self.request.user
        if user.Rol == 'Docente':
            from gestion_aulatec.models import Docente
            form.instance.IdDocente = Docente.objects.get(IdUsuario=user)
        form.instance.AnioLectivo = date.today().year
        messages.success(self.request, 'Calificación actualizada correctamente.')
        return super().form_valid(form)


class CalificacionDeleteView(EsAdminMixin, DeleteView):
    model = Calificacion
    template_name = 'gestion_aulatec/calificacion_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:calificacion_list')
    context_object_name = 'calificacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.Rol == 'Administrador':
            context['base_template'] = 'gestion_aulatec/base_admin.html'
        else:
            context['base_template'] = 'gestion_aulatec/base_docente.html'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Calificación eliminada correctamente.')
        return super().form_valid(form)