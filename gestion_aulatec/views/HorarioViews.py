# Archivo: gestion_aulatec/views/HorarioViews.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from gestion_aulatec.models import Horario, Grado, Materia, Docente
from gestion_aulatec.forms.HorarioForm import HorarioForm


class HorarioListView(ListView):
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


class HorarioCreateView(CreateView):
    model = Horario
    form_class = HorarioForm
    template_name = 'gestion_aulatec/horario_crear.html'
    success_url = reverse_lazy('gestion_aulatec:horario_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grados'] = Grado.objects.all()
        context['materias'] = Materia.objects.all()
        context['docentes'] = Docente.objects.all()
        context['dias'] = Horario.DIAS_SEMANA
        return context


class HorarioUpdateView(UpdateView):
    model = Horario
    form_class = HorarioForm
    template_name = 'gestion_aulatec/horario_editar.html'
    success_url = reverse_lazy('gestion_aulatec:horario_list')
    context_object_name = 'horario'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grados'] = Grado.objects.all()
        context['materias'] = Materia.objects.all()
        context['docentes'] = Docente.objects.all()
        context['dias'] = Horario.DIAS_SEMANA
        return context


class HorarioDeleteView(DeleteView):
    model = Horario
    template_name = 'gestion_aulatec/horario_eliminar.html'
    success_url = reverse_lazy('gestion_aulatec:horario_list')
    context_object_name = 'horario'
