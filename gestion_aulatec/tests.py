from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from .models import Usuario,Grado,Estudiante,Docente,Materia
#Casos de pruebas para la creación de usuarios.
class PruebasIntegracionUsuario(TestCase):

    def test_crear_usuario(self):
        datos_usuario = {
            'TipoId':'CC',
            'NumId':'0000',
            'Nombres':'Kevin',
            'Apellidos':'Valderrama',
            'Rol':'Administrador',
            'Celular':'3004897185',
            'password':'123456789',
            'password_confirm':'123456789'
        }
        
        url_registro = reverse('gestion_aulatec:usuario_create')
        response = self.client.post(url_registro, datos_usuario)

        self.assertTrue(Usuario.objects.filter(NumId='0000').exists())

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('gestion_aulatec:login'))

#Casos de pruebas de Inicio de Sesion
class PruebasInicioSesion(TestCase):
    def setUp(self):
        self.password = 'contraseña_encriptada'
        self.usuario_valido = Usuario.objects.create_user(
            NumId='0000',
            password = self.password,
            TipoId = 'CC',
            Nombres = 'Kevin',
            Apellidos = 'Valderrama',
            Rol = 'Administrador'
        )

    #pruebas de inicio de sesion existoso (credenciales correctas).
    def test_inicio_sesion_exitoso(self):

        login_exitoso = self.client.login(NumId='0000', password=self.password)

        self.assertTrue(login_exitoso)

        response = self.client.get(reverse('gestion_aulatec:admin_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'gestion_aulatec/admin_dashboard.html')
        self.assertContains(response, 'Kevin')

    #prueba de inicio de sesion fallido (credenciales falsas.).
    def test_inicio_sesion_fallido(self):

        login_fallido = self.client.login(NumId='0000', password='contraseña_incorrecta')

        self.assertFalse(login_fallido)

        response = self.client.get(reverse('gestion_aulatec:admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('gestion_aulatec:login')}?next={reverse('gestion_aulatec:admin_dashboard')}")


#Casos de pruebas para el modulo de grados.
class PruebasGestionGrados(TestCase):
    #Prueba creacion exitosa
    def test_creacion_exitosa_grado(self):
        datos = {
            'NumGrado': 3,
            'NumCurso': 'B'
        }

        url_registro = reverse('gestion_aulatec:grado_create')
        response = self.client.post(url_registro,datos)

        #verificamos la redirección
        self.assertEqual(response.status_code, 302)

        #verificamos que el grado este creado
        self.assertTrue(Grado.objects.filter(NumGrado = 3,NumCurso= 'B').exists())

    #Prueba creacion de grado fallido(falta de credenciales)
    def test_falla_por_datos_faltantes(self):
        datos = {
            'NumGrado': 3,
        }

        url_registro = reverse('gestion_aulatec:grado_create')
        response = self.client.post(url_registro,datos)

        #verificamos que no hubo redirección
        self.assertEqual(response.status_code, 200)

        #verificamos que el grado este creado
        self.assertFalse(Grado.objects.filter(NumGrado = 3).exists())

    #Prueba duplicación de grados(que no se creen dos grados con los mismos datos).
    def setUp(self):
        #crear un objeto grado en la base de datos
        Grado.objects.create(NumGrado=2, NumCurso='B')

    def test_falla_por_duplicacion(self):
        datos = {
            'NumGrado':2,
            'NumCurso':'B'
        }

        url_registro = reverse('gestion_aulatec:grado_create')
        response = self.client.post(url_registro,datos)

        #verificamos que no hubo redireccion 
        self.assertEqual(response.status_code, 200)

        #verificamos que solo hay un objeto con esas credenciales
        self.assertEqual(Grado.objects.filter(NumGrado=2,NumCurso='B').count(),1)

#Casos de prueba para el modulo de estudiante
class PruebasGestionEstudiantes(TestCase):
    #Creacion de objetos(Usuario,Grados)
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            NumId='0000',
            password = 'contraseña_encriptada',
            TipoId = 'CC',
            Nombres = 'Kevin',
            Apellidos = 'Valderrama',
            Rol = 'Estudiante'
        )

        self.grado = Grado.objects.create(NumGrado=2,NumCurso='B')

    #Prueba de creación exitosa
    def test_creacion_exitosa_estudiante(self):
        #datos de los objetos creados(usuario,grado)
        datos = {
           'IdUsuario' : self.usuario.IdUsuario,
           'IdGrado' : self.grado.IdGrado,
        }

        url_registro = reverse('gestion_aulatec:estudiante_create')
        response = self.client.post(url_registro,datos)

        #verificamos que la redirección sea exitosa
        self.assertEqual(response.status_code,302)

        #verificamos que el estudiante este creado
        self.assertTrue(Estudiante.objects.filter(IdUsuario=self.usuario, IdGrado=self.grado).exists())

    #prueba creacion de estudiante sin el campo grado
    def test_creacion_exitosa_sin_grado(self):
        datos = {
            'IdUsuario' : self.usuario.IdUsuario,
        } 

        url_registro = reverse('gestion_aulatec:estudiante_create')
        response = self.client.post(url_registro,datos)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Estudiante.objects.filter(IdUsuario=self.usuario).exists())

    #prueba con credenciales inexistentes
    def test_creacion_fallida_estudiante(self):
        grado_new = 12

        datos = {
            'IdUsuario': self.usuario.IdUsuario,
            'IdGrado': grado_new,
        }

        url_registro = reverse('gestion_aulatec:estudiante_create')
        response = self.client.post(url_registro,datos)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(Estudiante.objects.filter(IdUsuario = self.usuario).exists())

class PruebasGestionMateria(TestCase):
    def setUp(self):
        self.password = 'contraseña_encriptada'
        self.usuario_docente = Usuario.objects.create_user(
            NumId='0000',
            password = self.password,
            TipoId = 'CC',
            Nombres = 'Kevin',
            Apellidos = 'Valderrama',
            Rol = 'Docente'
        )

        self.docente = Docente.objects.create(
            IdUsuario=self.usuario_docente
        )

        self.materia_existente = Materia.objects.create(
            NombreMateria = 'Calculo',
            IdDocente = self.docente
        )
    #Prueba de creación exitosa 
    def test_creacion_existosa_materia(self):
        datos = {
            'NombreMateria' : 'Matematicas',
            'IdDocente' : self.docente.pk
        }

        response = self.client.post(reverse('gestion_aulatec:materia_create'), datos)

        #verificar la redireccion
        self.assertEqual(response.status_code,302)

        #verificar la creacion de la materia
        self.assertTrue(Materia.objects.filter(NombreMateria='Matematicas', IdDocente=self.docente).exists())

    #creacion de materia sin docente
    def test_creacion_existosa_sin_docente(self):
        datos = {
            'NombreMateria': 'Quimica',
        }
        response = self.client.post(reverse('gestion_aulatec:materia_create'), datos)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Materia.objects.filter(NombreMateria='Quimica', IdDocente__isnull=True).exists())

    def test_falla_por_nombre_duplicado(self):
        datos = {
            'NombreMateria': self.materia_existente.NombreMateria,
            'IdDocente': self.docente.pk,
        }
        response = self.client.post(reverse('gestion_aulatec:materia_create'), datos)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Materia.objects.filter(NombreMateria=self.materia_existente.NombreMateria).count(), 1)
        self.assertIn('NombreMateria', response.context['form'].errors)

        