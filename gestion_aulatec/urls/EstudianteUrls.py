from django.urls import path
from gestion_aulatec import views # importa las vistas del archivo views.py

urlpatterns = [
    # URLs para estudiante
    path('', views.EstudianteListView.as_view(), name='estudiante_list'),
    path('nuevo/', views.EstudianteCreateView.as_view(), name='estudiante_create'),
    path('<int:pk>/editar/', views.EstudianteUpdateView.as_view(), name='estudiante_update'),
    path('<int:pk>/eliminar/', views.EstudianteDeleteView.as_view(), name='estudiante_delete'),
]
