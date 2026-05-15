from django.urls import path
from gestion_aulatec import views

urlpatterns = [
    # URLs para grado
    path('', views.GradoListView.as_view(), name='grado_list'),
    path('nuevo/', views.GradoCreateView.as_view(), name='grado_create'),
    path('<int:pk>/editar/', views.GradoUpdateView.as_view(), name='grado_update'),
    path('<int:pk>/eliminar/', views.GradoDeleteView.as_view(), name='grado_delete'),
]