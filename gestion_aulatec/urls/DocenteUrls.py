from django.urls import path
from gestion_aulatec import views # importa las vistas del archivo views.py

urlpatterns = [
    # URLs para docente
    path('', views.DocenteListView.as_view(), name='docente_list'),
    path('nuevo/', views.DocenteCreateView.as_view(), name='docente_create'),
    path('<int:pk>/editar/', views.DocenteUpdateView.as_view(), name='docente_update'),
    path('<int:pk>/eliminar/', views.DocenteDeleteView.as_view(), name='docente_delete'),
]