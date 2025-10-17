from django.urls import path
from gestion_aulatec import views # importa las vistas del archivo views.py

urlpatterns = [
    # URL para listar todos los usuarios
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    # URL para crear un nuevo usuario
    path('usuarios/nuevo/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    # URL para actualizar un usuario existente (pk es la clave primaria)
    path('usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    # URL para eliminar un usuario existente
    path('usuarios/<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
]