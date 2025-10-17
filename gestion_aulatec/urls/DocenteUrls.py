from django.urls import path
from gestion_aulatec import views # importa las vistas del archivo views.py

urlpatterns = [
    # URLs para docente
    path('docentes/', views.DocenteListView.as_view(), name='docente_list'),
    path('docentes/nuevo/', views.DocenteCreateView.as_view(), name='docente_create'),
    path('docentes/<int:pk>/editar/', views.DocenteUpdateView.as_view(), name='docente_update'),
    path('docentes/<int:pk>/eliminar/', views.DocenteDeleteView.as_view(), name='docente_delete'),

]