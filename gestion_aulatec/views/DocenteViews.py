from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from gestion_aulatec.models import Docente
from gestion_aulatec.forms import DocenteForm


class EsAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('gestion_aulatec:login')
        return redirect('gestion_aulatec:home')


class DocenteListView(EsAdminMixin, ListView):
    model = Docente
    template_name = 'gestion_aulatec/docente_list.html'
    context_object_name = 'docentes'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(IdUsuario__Nombres__icontains=query) |
                Q(IdUsuario__Apellidos__icontains=query)
            )
        return queryset.order_by('IdUsuario__Nombres', 'IdUsuario__Apellidos')


class DocenteCreateView(EsAdminMixin, CreateView):
    model = Docente
    form_class = DocenteForm
    template_name = 'gestion_aulatec/docente_form.html'
    success_url = reverse_lazy('gestion_aulatec:docente_list')


class DocenteUpdateView(EsAdminMixin, UpdateView):
    model = Docente
    form_class = DocenteForm
    template_name = 'gestion_aulatec/docente_form.html'
    success_url = reverse_lazy('gestion_aulatec:docente_list')


class DocenteDeleteView(EsAdminMixin, DeleteView):
    model = Docente
    template_name = 'gestion_aulatec/docente_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:docente_list')
    context_object_name = 'docente'
