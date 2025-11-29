from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.db.models import Q
from django.urls import reverse_lazy

from gestion_aulatec.models import Materia
from gestion_aulatec.forms import MateriaForm

# Vistas para el CRUD de materia

#Leer (Listar todas las materias)
class MateriaListView(ListView):
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
    
# Crear un nueva Materia
class MateriaCreateView(CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_aulatec/materia_form.html'
    success_url = reverse_lazy('gestion_aulatec:materia_list')

# Actualizar una Materia Existente
class MateriaUpdateView(UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_aulatec/materia_form.html'
    success_url = reverse_lazy('gestion_aulatec:materia_list')

# Eliminar una materia 
class MateriaDeleteView(DeleteView):
    model = Materia
    template_name = 'gestion_aulatec/materia_confirm_delete.html'
    success_url = reverse_lazy('gestion_aulatec:materia_list')
    context_object_name = 'materia'
