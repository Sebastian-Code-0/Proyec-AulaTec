from django.urls import path
from gestion_aulatec import views  # importa las vistas del archivo views.py
from gestion_aulatec.views.MatriculaViews import toggle_matricula_activa, ExportarMatriculasExcelView
urlpatterns = [
    # URLs para matrícula
    path('nueva/', views.MatriculaCreateView.as_view(), name='matricula_form'),
    path('', views.MatriculaListView.as_view(), name='matricula_list'),
    path('<int:pk>/detalles/', views.MatriculaDetailView.as_view(), name='matricula_detail'),
    path('<int:pk>/editar/', views.MatriculaUpdateView.as_view(), name='matricula_update'),
    path('<int:pk>/eliminar/', views.MatriculaDeleteView.as_view(), name='matricula_delete'),
    path('toggle/<int:pk>/', toggle_matricula_activa, name='matricula_toggle'),
    path('exportar/excel/', ExportarMatriculasExcelView.as_view(), name='exportar_matriculas_excel'),
]