from django.urls import path
from gestion_aulatec import views

urlpatterns = [
    path('', views.CalificacionListView.as_view(), name='calificacion_list'),
    path('nuevo/', views.CalificacionCreateView.as_view(), name='calificacion_create'),
    path('<int:pk>/editar/', views.CalificacionUpdateView.as_view(), name='calificacion_update'),
    path('<int:pk>/eliminar/', views.CalificacionDeleteView.as_view(), name='calificacion_delete'),
    path('estudiante/', views.CalificacionEstudianteView.as_view(), name='calificacion_estudiante'),
    path('estudiante/<int:pk>/', views.CalificacionEstudianteView.as_view(), name='calificacion_estudiante_detail'),
]