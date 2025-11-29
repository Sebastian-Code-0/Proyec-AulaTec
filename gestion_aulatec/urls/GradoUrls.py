from django.urls import path
from gestion_aulatec import views
from gestion_aulatec.views import GradoListView, GradoCreateView, GradoUpdateView, GradoDeleteView
urlpatterns = [
    path('', GradoListView.as_view(), name='grado_list'),
    path('nuevo/', GradoCreateView.as_view(), name='grado_create'),
    path('<int:pk>/editar/', GradoUpdateView.as_view(), name='grado_update'),
    path('<int:pk>/eliminar/', GradoDeleteView.as_view(), name='grado_delete'),
]