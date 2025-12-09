from django.urls import path
from gestion_aulatec import views

urlpatterns = [
    # URLs para grado
    path('grados/', views.GradoListView.as_view(), name='grado_list'),
    path('grados/nuevo/', views.GradoCreateView.as_view(), name='grado_create'),
    path('grados/<int:pk>/editar/', views.GradoUpdateView.as_view(), name='grado_update'),
    path('grados/<int:pk>/eliminar/', views.GradoDeleteView.as_view(), name='grado_delete'),

]