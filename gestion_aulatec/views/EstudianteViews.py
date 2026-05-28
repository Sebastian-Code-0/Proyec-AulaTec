from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from gestion_aulatec.models import Estudiante
from gestion_aulatec.forms import EstudianteForm


class EsAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('gestion_aulatec:login')
        return redirect('gestion_aulatec:home')


class EstudianteListView(EsAdminMixin, ListView):
    model = Estudiante
    template_name = 'gestion_aulatec/estudiante_list.html'
    context_object_name = 'estudiantes'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('IdUsuario', 'IdGrado')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(IdUsuario__Nombres__icontains=query) |
                Q(IdUsuario__Apellidos__icontains=query)
            )
        return queryset.order_by('IdUsuario__Nombres', 'IdUsuario__Apellidos')


class EstudianteCreateView(EsAdminMixin, CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'gestion_aulatec/estudiante_form.html'
    success_url = reverse_lazy('gestion_aulatec:estudiante_list')


class EstudianteUpdateView(EsAdminMixin, UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'gestion_aulatec/estudiante_form.html'
    success_url = reverse_lazy('gestion_aulatec:estudiante_list')


class EstudianteDeleteView(EsAdminMixin, DeleteView):
    model = Estudiante
    template_name = 'gestion_aulatec/estudiante_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:estudiante_list')
    context_object_name = 'estudiante'
