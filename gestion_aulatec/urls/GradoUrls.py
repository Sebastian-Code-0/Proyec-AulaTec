from django.urls import path
from gestion_aulatec import views
<<<<<<< HEAD
from gestion_aulatec.views import GradoListView, GradoCreateView, GradoUpdateView, GradoDeleteView
urlpatterns = [
    path('', GradoListView.as_view(), name='grado_list'),
    path('nuevo/', GradoCreateView.as_view(), name='grado_create'),
    path('<int:pk>/editar/', GradoUpdateView.as_view(), name='grado_update'),
    path('<int:pk>/eliminar/', GradoDeleteView.as_view(), name='grado_delete'),
=======

urlpatterns = [
    # URLs para grado
    path('grados/', views.GradoListView.as_view(), name='grado_list'),
    path('grados/nuevo/', views.GradoCreateView.as_view(), name='grado_create'),
    path('grados/<int:pk>/editar/', views.GradoUpdateView.as_view(), name='grado_update'),
    path('grados/<int:pk>/eliminar/', views.GradoDeleteView.as_view(), name='grado_delete'),

>>>>>>> 4e2f81b62d3d85f4ea86504f7061355e11f3faf0
]