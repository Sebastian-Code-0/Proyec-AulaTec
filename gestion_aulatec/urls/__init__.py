from django.urls import path,include
from gestion_aulatec.views.LoginViews import home_view

app_name = 'gestion_aulatec'



urlpatterns = [
    path("",home_view, name='home'),
    path("grados/", include("gestion_aulatec.urls.GradoUrls")),
    path("docentes/", include("gestion_aulatec.urls.DocenteUrls")),
    path("estudiantes/", include("gestion_aulatec.urls.EstudianteUrls")),
    path("materia/", include("gestion_aulatec.urls.MateriaUrls")),
    path("horarios/", include("gestion_aulatec.urls.HorarioUrls")),
    path("matricula/", include("gestion_aulatec.urls.MatriculaUrls")),
    path("usuario/", include("gestion_aulatec.urls.UsuarioUrls")),
    path("login/", include("gestion_aulatec.urls.LoginUrls"))
]