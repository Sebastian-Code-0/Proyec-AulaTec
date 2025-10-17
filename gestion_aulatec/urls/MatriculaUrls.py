from django.urls import path
from gestion_aulatec import views  # importa las vistas del archivo views.py
from gestion_aulatec.views.MatriculaViews import toggle_matricula_activa 
urlpatterns = [
    # URLs para matrícula
    path('matriculas/nueva/', views.MatriculaCreateView.as_view(), name='matricula_form'),
    path('matriculas/', views.MatriculaListView.as_view(), name='matricula_list'),
    path('matriculas/<int:pk>/detalles/', views.MatriculaDetailView.as_view(), name='matricula_detail'),
    path('matriculas/<int:pk>/editar/', views.MatriculaUpdateView.as_view(), name='matricula_update'),
    path('matriculas/<int:pk>/eliminar/', views.MatriculaDeleteView.as_view(), name='matricula_delete'),
    path('matriculas/toggles/<int:pk>', toggle_matricula_activa, name='matricula_toggle'),
]