from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from gestion_aulatec.models import Materia
from gestion_aulatec.forms import MateriaForm


class EsAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.Rol == 'Administrador'

    def handle_no_permission(self):
        return redirect('gestion_aulatec:home')


class MateriaListView(EsAdminMixin, ListView):
    model = Materia
    template_name = 'gestion_aulatec/materia_list.html'
    context_object_name = 'materias'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(NombreMateria__icontains=query) |
                Q(IdDocente__IdUsuario__Nombres__icontains=query) |
                Q(IdDocente__IdUsuario__Apellidos__icontains=query)
            )
        return queryset.order_by('NombreMateria')


class MateriaCreateView(EsAdminMixin, CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_aulatec/materia_form.html'
    success_url = reverse_lazy('gestion_aulatec:materia_list')


class MateriaUpdateView(EsAdminMixin, UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_aulatec/materia_form.html'
    success_url = reverse_lazy('gestion_aulatec:materia_list')


class MateriaDeleteView(EsAdminMixin, DeleteView):
    model = Materia
    template_name = 'gestion_aulatec/materia_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:materia_list')
    context_object_name = 'materia'
