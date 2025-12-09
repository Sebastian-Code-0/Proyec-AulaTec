from django.urls import path
from gestion_aulatec import views # importa las vistas del archivo views.py

urlpatterns = [
 # URLs para materia
    path('materias/', views.MateriaListView.as_view(), name='materia_list'),
    path('materias/nuevo/', views.MateriaCreateView.as_view(), name='materia_create'),
    path('materias/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia_update'),
    path('materias/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia_delete'),
]    