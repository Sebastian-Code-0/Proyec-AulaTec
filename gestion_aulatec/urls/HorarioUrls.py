# Archivo: gestion_aulatec/urls/HorarioUrls.py

from django.urls import path
from gestion_aulatec import views

urlpatterns = [
    # URLs para horario
    path('', views.HorarioListView.as_view(), name='horario_list'),
    path('listar/', views.HorarioListView.as_view(), name='listar_horarios'),
    path('crear/', views.HorarioCreateView.as_view(), name='horario_create'),
    path('crear/', views.HorarioCreateView.as_view(), name='crear_horario'),
    path('<int:pk>/editar/', views.HorarioUpdateView.as_view(), name='horario_update'),
    path('<int:pk>/editar/', views.HorarioUpdateView.as_view(), name='editar_horario'),
    path('<int:pk>/eliminar/', views.HorarioDeleteView.as_view(), name='horario_delete'),
    path('<int:pk>/eliminar/', views.HorarioDeleteView.as_view(), name='eliminar_horario'),
]