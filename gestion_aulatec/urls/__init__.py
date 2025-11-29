from django.urls import path,include
from gestion_aulatec.views.LoginViews import home_view
<<<<<<< HEAD
from gestion_aulatec.views.GradoViews import GradoListView

app_name = 'gestion_aulatec'

=======

app_name = 'gestion_aulatec'



>>>>>>> 4e2f81b62d3d85f4ea86504f7061355e11f3faf0
urlpatterns = [
    path("",home_view, name='home'),
    path("grados/", include("gestion_aulatec.urls.GradoUrls")),
    path("docentes/", include("gestion_aulatec.urls.DocenteUrls")),
    path("estudiantes/", include("gestion_aulatec.urls.EstudianteUrls")),
    path("materia/", include("gestion_aulatec.urls.MateriaUrls")),
    path("matricula/", include("gestion_aulatec.urls.MatriculaUrls")),
    path("usuario/", include("gestion_aulatec.urls.UsuarioUrls")),
<<<<<<< HEAD
    path("login/", include("gestion_aulatec.urls.LoginUrls")),
    path("certificados/", include("gestion_aulatec.urls.CertificadoUrls")),
    path("prueba/", include("gestion_aulatec.urls.TestUrls")),
    path("test-grados/", GradoListView.as_view(), name="test_grado_list"),
=======
    path("login/", include("gestion_aulatec.urls.LoginUrls"))
>>>>>>> 4e2f81b62d3d85f4ea86504f7061355e11f3faf0
]