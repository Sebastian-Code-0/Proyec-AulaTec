from django.urls import path
from gestion_aulatec import views # importa las vistas del archivo views.py

urlpatterns = [
    # URLs para usuario
    path('', views.UsuarioListView.as_view(), name='usuario_list'),
    path('nuevo/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
    path('cambiar-password/', views.CambiarPasswordView.as_view(), name='cambiar_password'),
]