from django.urls import path
from gestion_aulatec import views # importa las vistas del archivo views.py

urlpatterns = [
    # URLs para materia
    path('', views.MateriaListView.as_view(), name='materia_list'),
    path('nuevo/', views.MateriaCreateView.as_view(), name='materia_create'),
    path('<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia_update'),
    path('<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia_delete'),
]
