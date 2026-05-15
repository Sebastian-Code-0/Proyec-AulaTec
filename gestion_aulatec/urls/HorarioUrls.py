# Archivo: gestion_aulatec/urls/HorarioUrls.py

from django.urls import path
from gestion_aulatec import views

urlpatterns = [
    # URLs para horario
    path('', views.HorarioListView.as_view(), name='horario_list'),
    path('crear/', views.HorarioCreateView.as_view(), name='horario_create'),
    path('<int:pk>/editar/', views.HorarioUpdateView.as_view(), name='horario_update'),
    path('<int:pk>/eliminar/', views.HorarioDeleteView.as_view(), name='horario_delete'),
]