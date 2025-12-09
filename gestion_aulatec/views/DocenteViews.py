from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView
from django.db.models import Q
from django.urls import reverse_lazy

from gestion_aulatec.models import Docente
from gestion_aulatec.forms import DocenteForm

#Vistas para el CRUD de Docentes

#Leer (Listar todos los docentes)
class DocenteListView(ListView):
    model = Docente
    template_name = 'gestion_aulatec/docente_list.html' # Nueva plantilla
    context_object_name = 'docentes' # Nombre de la variable en la plantilla

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            # Filtra por Nombres o Apellidos del Usuario asociado
            queryset = queryset.filter(
                Q(IdUsuario__Nombres__icontains=query) |
                Q(IdUsuario__Apellidos__icontains=query)
            )
        return queryset.order_by('IdUsuario__Nombres', 'IdUsuario__Apellidos')

# 2. Crear un nuevo Docente
class DocenteCreateView(CreateView):
    model = Docente
    form_class = DocenteForm
    template_name = 'gestion_aulatec/docente_form.html' # Nueva plantilla
    success_url = reverse_lazy('gestion_aulatec:docente_list') # Redirige a la lista de docentes

# 3. Actualizar un Docente existente
class DocenteUpdateView(UpdateView):
    model = Docente
    form_class = DocenteForm
    template_name = 'gestion_aulatec/docente_form.html' # Reusa la misma plantilla
    success_url = reverse_lazy('gestion_aulatec:docente_list')

# 4. Eliminar un Docente
class DocenteDeleteView(DeleteView):
    model = Docente
    template_name = 'gestion_aulatec/docente_confirm_delete.html' # Nueva plantilla
    success_url = reverse_lazy('gestion_aulatec:docente_list')
    context_object_name = 'docente' # Para usar {{ docente.IdUsuario.Nombres }} en el template
