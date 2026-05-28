from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.db.models import Q

from gestion_aulatec.models import Horario, Grado, Materia, Docente
from gestion_aulatec.forms.HorarioForm import HorarioForm


class EsAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('gestion_aulatec:login')
        return redirect('gestion_aulatec:home')


class HorarioListView(EsAdminMixin, ListView):
    model = Horario
    template_name = 'gestion_aulatec/horario_list.html'
    context_object_name = 'horarios'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(grado__NumGrado__icontains=query) |
                Q(grado__NumCurso__icontains=query) |
                Q(materia__NombreMateria__icontains=query) |
                Q(docente__IdUsuario__Nombres__icontains=query) |
                Q(docente__IdUsuario__Apellidos__icontains=query) |
                Q(dia_semana__icontains=query)
            )
        return queryset.order_by('dia_semana', 'hora_inicio')


class HorarioCreateView(EsAdminMixin, CreateView):
    model = Horario
    form_class = HorarioForm
    template_name = 'gestion_aulatec/horario_crear.html'
    success_url = reverse_lazy('gestion_aulatec:horario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grados'] = Grado.objects.all()
        context['materias'] = Materia.objects.all()
        context['docentes'] = Docente.objects.select_related('IdUsuario').all()
        context['dias'] = Horario.DIAS_SEMANA
        return context


class HorarioUpdateView(EsAdminMixin, UpdateView):
    model = Horario
    form_class = HorarioForm
    template_name = 'gestion_aulatec/horario_editar.html'
    success_url = reverse_lazy('gestion_aulatec:horario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grados'] = Grado.objects.all()
        context['materias'] = Materia.objects.all()
        context['docentes'] = Docente.objects.select_related('IdUsuario').all()
        context['dias'] = Horario.DIAS_SEMANA
        return context


class HorarioDeleteView(EsAdminMixin, DeleteView):
    model = Horario
    template_name = 'gestion_aulatec/horario_eliminar.html'
    success_url = reverse_lazy('gestion_aulatec:horario_list')
