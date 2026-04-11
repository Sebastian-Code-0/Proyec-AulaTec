from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from gestion_aulatec.models import Grado
from gestion_aulatec.forms import GradoForm
#--Vistas para el CRUD de Grado---

#leer
class GradoListView(LoginRequiredMixin, ListView):
    model = Grado
    template_name = 'gestion_aulatec/grado_list.html'
    context_object_name = 'grados'

#Crear
class GradoCreateView(LoginRequiredMixin, CreateView):
    model = Grado
    form_class = GradoForm
    template_name = 'gestion_aulatec/grado_form.html'
    success_url = reverse_lazy('gestion_aulatec:grado_list')

#Actualizar
class GradoUpdateView(LoginRequiredMixin, UpdateView):
    model = Grado
    form_class = GradoForm
    template_name = 'gestion_aulatec/grado_form.html'
    success_url = reverse_lazy('gestion_aulatec:grado_list')

#Eliminar
class GradoDeleteView(LoginRequiredMixin, DeleteView):
    model = Grado
    template_name = 'gestion_aulatec/grado_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:grado_list')
    
    context_object_name = 'grado'