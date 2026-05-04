from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.db.models import Count

from gestion_aulatec.models import Grado
from gestion_aulatec.forms import GradoForm


class EsAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')


class GradoListView(EsAdminMixin, ListView):
    model = Grado
    template_name = 'gestion_aulatec/grado_list.html'
    context_object_name = 'grados'

    def get_queryset(self):
        return Grado.objects.annotate(total_estudiantes=Count('estudiante'))


class GradoCreateView(EsAdminMixin, CreateView):
    model = Grado
    form_class = GradoForm
    template_name = 'gestion_aulatec/grado_form.html'
    success_url = reverse_lazy('gestion_aulatec:grado_list')


class GradoUpdateView(EsAdminMixin, UpdateView):
    model = Grado
    form_class = GradoForm
    template_name = 'gestion_aulatec/grado_form.html'
    success_url = reverse_lazy('gestion_aulatec:grado_list')


class GradoDeleteView(EsAdminMixin, DeleteView):
    model = Grado
    template_name = 'gestion_aulatec/grado_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:grado_list')
    context_object_name = 'grado'
