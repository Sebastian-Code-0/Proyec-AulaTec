from django.urls import path
from gestion_aulatec import views  

urlpatterns = [
    # URL para la autenticación (SIN el home aquí)
    path('', views.login_view, name='login'),  # /login/ va directo al login
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/docente/', views.DocenteDashboardView.as_view(), name='docente_dashboard'),
    path('dashboard/estudiante/', views.EstudianteDashboardView.as_view(), name='estudiante_dashboard'),
]