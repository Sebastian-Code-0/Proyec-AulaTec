# Conceptos Técnicos — AulaTec
### Guía de estudio para la presentación final

> Todos los ejemplos usan código real del proyecto, principalmente del módulo de Calificaciones.

---

## 1. ¿Qué es Django?

Django es un **framework web de Python**. Un framework es un conjunto de herramientas y reglas predefinidas que facilitan construir aplicaciones sin tener que programar todo desde cero.

Django incluye de serie:
- ORM (acceso a base de datos sin escribir SQL)
- Sistema de autenticación y sesiones
- Protección contra ataques comunes (CSRF, XSS, inyección SQL)
- Sistema de plantillas HTML
- Panel de administración automático

---

## 2. El patrón MVT (Model – View – Template)

Django sigue el patrón **MVT**, que es la versión de Django del clásico MVC (Model-View-Controller). Define cómo se organiza y fluye la información en la aplicación.

```
NAVEGADOR  →  URL  →  VIEW  →  MODEL  →  BASE DE DATOS
                         ↓
                     TEMPLATE  →  NAVEGADOR
```

### ¿Qué hace cada parte?

| Capa | Archivo en el proyecto | Responsabilidad |
|---|---|---|
| **Model** | `models/calificacion.py` | Define la estructura de los datos y reglas de negocio |
| **View** | `views/calificacion_views.py` | Recibe la petición, consulta el modelo, prepara los datos |
| **Template** | `templates/.../calificacion_list.html` | Muestra los datos en HTML al usuario |

### Flujo completo de una petición — ejemplo real

Cuando un docente abre `/calificaciones/`:

```
1. El navegador hace GET /calificaciones/
2. Django busca en urls/__init__.py → CalificacionUrls.py
3. Encuentra que esa URL usa CalificacionListView
4. CalificacionListView.get_queryset() consulta la BD:
      Calificacion.objects.filter(IdDocente__IdUsuario=user)
5. Los datos se pasan al template calificacion_list.html
6. El template genera el HTML con las calificaciones
7. El HTML llega al navegador del docente
```

---

## 3. El Model — `models/calificacion.py`

Un **Model** es una clase de Python que representa una tabla en la base de datos. Cada atributo de la clase es una columna de la tabla.

```python
# gestion_aulatec/models/calificacion.py

class Calificacion(models.Model):

    PERIODOS = [
        (1, 'Primer Periodo'),
        (2, 'Segundo Periodo'),
        (3, 'Tercer Periodo'),
        (4, 'Cuarto Periodo'),
    ]

    IdCalificacion = models.AutoField(primary_key=True)
    IdEstudiante   = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    IdMateria      = models.ForeignKey(Materia,    on_delete=models.CASCADE)
    IdDocente      = models.ForeignKey(Docente,    on_delete=models.SET_NULL, null=True)
    AnioLectivo    = models.IntegerField()
    Periodo        = models.IntegerField(choices=PERIODOS)
    NombreActividad= models.CharField(max_length=100)
    Nota           = models.DecimalField(max_digits=4, decimal_places=2)
    Observaciones  = models.TextField(blank=True, null=True)
    FechaRegistro  = models.DateTimeField(auto_now_add=True)
```

### ¿Qué significa cada tipo de campo?

| Campo | Tipo | Qué guarda |
|---|---|---|
| `AutoField` | Entero autoincremental | El ID único (1, 2, 3...) |
| `ForeignKey` | Relación | El ID de otro registro en otra tabla |
| `IntegerField` | Número entero | Año lectivo, período |
| `CharField` | Texto corto | Nombre de actividad |
| `DecimalField` | Número decimal | La nota (ej: 8.50) |
| `TextField` | Texto largo | Observaciones |
| `DateTimeField` | Fecha + hora | Cuándo se registró |

### ¿Qué es un objeto?

Un **objeto** es una instancia concreta de la clase. Si `Calificacion` es el molde, un objeto es una calificación real guardada en la BD:

```python
# Esto es la CLASE (el molde):
class Calificacion(models.Model):
    ...

# Esto es un OBJETO (una calificación real):
cal = Calificacion(
    IdEstudiante = estudiante,
    IdMateria    = materia,
    Periodo      = 2,
    NombreActividad = "Examen Parcial",
    Nota         = 8.50
)
cal.save()  # Lo guarda en la base de datos
```

### Meta — configuración extra del modelo

```python
class Meta:
    db_table = 'Calificacion'           # nombre real de la tabla en MariaDB
    ordering = ['AnioLectivo', 'Periodo']  # orden por defecto al consultar
    unique_together = (                  # combinación que no puede repetirse
        'IdEstudiante', 'IdMateria',
        'AnioLectivo', 'Periodo', 'NombreActividad'
    )
```

`unique_together` es una **restricción de integridad**: impide que el mismo estudiante tenga dos notas con el mismo nombre de actividad en el mismo período y materia del mismo año.

---

## 4. ForeignKey — Relaciones entre tablas

Una `ForeignKey` es una relación entre dos tablas. Significa "este campo apunta a un registro de otra tabla".

```python
IdEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
```

Esto significa:
- `Calificacion` pertenece a un `Estudiante`
- En la BD, guarda el ID del estudiante (`IdEstudiante_id`)
- `on_delete=CASCADE` → si se borra el estudiante, se borran sus calificaciones también

### Los tres tipos de `on_delete` usados en el proyecto

| Valor | Comportamiento |
|---|---|
| `CASCADE` | Borra en cadena (borra calificaciones si se borra el estudiante) |
| `SET_NULL` | Pone NULL (si se borra el docente, la calificación queda sin docente) |
| `PROTECT` | No deja borrar si hay registros relacionados |

### Cómo acceder a datos relacionados

```python
cal = Calificacion.objects.first()

# Acceder al nombre del estudiante (navegar la relación)
cal.IdEstudiante.IdUsuario.Nombres    # "Karen Fernanda"

# Acceder al nombre de la materia
cal.IdMateria.NombreMateria           # "Fisica"

# Acceder al nombre del docente
cal.IdDocente.IdUsuario.Nombres       # "Leidy"
```

Cada `.` navega hacia la tabla relacionada sin escribir un solo JOIN en SQL.

---

## 5. El ORM — Object Relational Mapper

El ORM es el sistema de Django que permite **interactuar con la base de datos escribiendo Python** en vez de SQL. Traduce automáticamente las instrucciones Python a consultas SQL.

### Equivalencias Python → SQL

```python
# CREAR un registro
Calificacion.objects.create(
    IdEstudiante=est, IdMateria=mat, Periodo=1, Nota=8.0
)
# SQL equivalente:
# INSERT INTO Calificacion (IdEstudiante_id, IdMateria_id, Periodo, Nota)
# VALUES (12, 7, 1, 8.0)

# LEER todos los registros
Calificacion.objects.all()
# SQL: SELECT * FROM Calificacion

# FILTRAR registros
Calificacion.objects.filter(Periodo=2)
# SQL: SELECT * FROM Calificacion WHERE Periodo = 2

# FILTRAR con relación (JOIN automático)
Calificacion.objects.filter(IdDocente__IdUsuario=request.user)
# SQL: SELECT c.* FROM Calificacion c
#      JOIN Docente d ON c.IdDocente_id = d.IdDocente
#      JOIN Usuario u ON d.IdUsuario_id = u.IdUsuario
#      WHERE u.IdUsuario = <id_del_usuario>

# OBTENER un solo registro
Calificacion.objects.get(pk=5)
# SQL: SELECT * FROM Calificacion WHERE IdCalificacion = 5

# ACTUALIZAR
cal = Calificacion.objects.get(pk=5)
cal.Nota = 9.0
cal.save()
# SQL: UPDATE Calificacion SET Nota = 9.0 WHERE IdCalificacion = 5

# ELIMINAR
Calificacion.objects.get(pk=5).delete()
# SQL: DELETE FROM Calificacion WHERE IdCalificacion = 5

# CONTAR registros
Calificacion.objects.filter(IdDocente=docente).count()
# SQL: SELECT COUNT(*) FROM Calificacion WHERE IdDocente_id = <id>

# PROMEDIO (aggregate)
from django.db.models import Avg
Calificacion.objects.filter(Periodo=1).aggregate(Avg('Nota'))
# SQL: SELECT AVG(Nota) FROM Calificacion WHERE Periodo = 1
```

### ¿Qué es un QuerySet?

Un `QuerySet` es el resultado de una consulta ORM. No ejecuta la consulta de inmediato — es **lazy** (perezosa), espera hasta que realmente se necesiten los datos.

```python
# Esto NO va a la BD todavía:
qs = Calificacion.objects.filter(Periodo=2)

# Esto SÍ ejecuta la consulta (al iterar o usar los datos):
for cal in qs:
    print(cal.Nota)
```

### El doble guión bajo `__` en los filtros

El `__` se usa para navegar relaciones o aplicar comparadores:

```python
# Navegar relación (JOIN)
Calificacion.objects.filter(IdDocente__IdUsuario=user)
#                                    ^ sigue la FK hasta IdUsuario

# Comparadores
Calificacion.objects.filter(Nota__gte=7.0)    # Nota >= 7.0
Calificacion.objects.filter(Nota__lt=5.0)     # Nota < 5.0
Calificacion.objects.filter(Nota__between=(5, 8))  # no existe, usar range
Calificacion.objects.filter(NombreActividad__icontains="examen")  # LIKE %examen%
```

---

## 6. La View — `views/calificacion_views.py`

Una **View** (vista) es la función o clase que recibe una petición HTTP, consulta el modelo y devuelve una respuesta (normalmente un HTML generado desde una template).

AulaTec usa **Class-Based Views (CBV)** — vistas basadas en clases. Django tiene clases predefinidas para las operaciones más comunes:

| Clase Django | Para qué sirve |
|---|---|
| `ListView` | Mostrar una lista de registros |
| `CreateView` | Mostrar formulario y guardar nuevo registro |
| `UpdateView` | Mostrar formulario y actualizar registro existente |
| `DeleteView` | Confirmar y eliminar un registro |
| `DetailView` | Mostrar el detalle de un registro |

### Ejemplo real — CalificacionListView

```python
class CalificacionListView(DocenteVinculadoMixin, EsDocenteOAdminMixin, ListView):
    model = Calificacion
    template_name = 'gestion_aulatec/calificacion_list.html'
    context_object_name = 'calificaciones'

    def get_queryset(self):
        user = self.request.user
        # Admin ve todo, docente solo ve las suyas
        if user.Rol == 'Administrador':
            qs = Calificacion.objects.all()
        else:
            qs = Calificacion.objects.filter(IdDocente__IdUsuario=user)

        # Filtros opcionales desde la URL (?periodo=2)
        periodo = self.request.GET.get('periodo')
        if periodo:
            qs = qs.filter(Periodo=periodo)

        return qs.order_by('AnioLectivo', 'Periodo')
```

### ¿Qué son los Mixins?

Un **Mixin** es una clase que agrega comportamiento extra a la vista. Se usan heredando de ellos.

```python
class CalificacionListView(DocenteVinculadoMixin, EsDocenteOAdminMixin, ListView):
#                          ^Mixin propio          ^Mixin propio       ^Clase Django
```

Los mixins de AulaTec:

```python
class EsDocenteOAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Esta función decide si el usuario puede acceder
        return self.request.user.Rol in ['Administrador', 'Docente']

    def handle_no_permission(self):
        # Si no puede acceder: redirige a login si no hay sesión,
        # o a home si tiene sesión pero rol incorrecto
        if not self.request.user.is_authenticated:
            return redirect('gestion_aulatec:login')
        return redirect('gestion_aulatec:home')
```

### get_context_data — pasar datos al template

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    # Agrego datos extra que el template va a necesitar
    context['periodos'] = [
        (1, 'Primer Periodo'),
        (2, 'Segundo Periodo'),
        (3, 'Tercer Periodo'),
        (4, 'Cuarto Periodo'),
    ]
    context['materias'] = Materia.objects.all()

    return context
```

El `context` es un diccionario Python que se le entrega al template. Cada clave del diccionario se convierte en una variable disponible en el HTML.

---

## 7. El Form — `forms/CalificacionForm.py`

Un **Form** es una clase que define los campos de un formulario HTML, sus validaciones y cómo se relacionan con el modelo.

```python
class CalificacionForm(forms.ModelForm):

    class Meta:
        model = Calificacion
        # Campos que aparecen en el formulario
        exclude = ['IdCalificacion', 'FechaRegistro', 'FechaActualizacion', 'AnioLectivo']
        widgets = {
            'Nota': forms.NumberInput(attrs={'min': '0', 'max': '10', 'step': '0.01'}),
        }

    def clean_Nota(self):
        # Validación personalizada del campo Nota
        nota = self.cleaned_data.get('Nota')
        if nota is not None:
            if nota < 0 or nota > 10:
                raise forms.ValidationError('La nota debe estar entre 0.00 y 10.00.')
        return nota

    def clean(self):
        # Validación que involucra varios campos a la vez
        cleaned_data = super().clean()
        # Verifica que no exista ya esa calificación (duplicado)
        # Si existe, lanza error antes de llegar a la BD
        ...
```

### Flujo de un formulario (POST)

```
Usuario llena el form → hace clic en Guardar
        ↓
Vista recibe POST → crea CalificacionForm(request.POST)
        ↓
form.is_valid() → llama a clean_Nota() y clean()
        ↓
Si válido: form.save() guarda en BD → redirect a la lista
Si inválido: re-renderiza el template con los errores marcados
```

---

## 8. La Template

Una **template** es un archivo HTML con etiquetas especiales de Django que permiten mostrar datos dinámicos.

```html
<!-- templates/gestion_aulatec/calificacion_list.html -->

{% for calificacion in calificaciones %}
    <tr>
        <td>{{ calificacion.IdEstudiante.IdUsuario.Nombres }}</td>
        <td>{{ calificacion.IdMateria.NombreMateria }}</td>
        <td>{{ calificacion.get_Periodo_display }}</td>
        <td>{{ calificacion.Nota }}</td>
    </tr>
{% empty %}
    <tr><td colspan="4">No hay calificaciones registradas.</td></tr>
{% endfor %}
```

### Etiquetas de Django en templates

| Etiqueta | Para qué sirve |
|---|---|
| `{{ variable }}` | Mostrar el valor de una variable |
| `{% for x in lista %}` | Iterar una lista |
| `{% if condicion %}` | Condicional |
| `{% url 'nombre_url' %}` | Generar una URL por nombre |
| `{% csrf_token %}` | Token de seguridad en formularios POST |
| `{% extends 'base.html' %}` | Heredar de otra plantilla |
| `{% block contenido %}` | Definir una sección reemplazable |
| `{% load static %}` | Cargar archivos estáticos (CSS, JS) |

### get_Periodo_display

```python
{{ calificacion.get_Periodo_display }}
```

Cuando un campo tiene `choices` (opciones), Django crea automáticamente un método `get_CAMPO_display()` que devuelve el texto legible en vez del valor numérico. Ej: `2` → `"Segundo Periodo"`.

---

## 9. Las URLs — enrutamiento

Django conecta cada URL con su vista a través de los archivos de URLs.

```python
# gestion_aulatec/urls/CalificacionUrls.py

urlpatterns = [
    path('',                    CalificacionListView.as_view(),   name='calificacion_list'),
    path('nuevo/',              CalificacionCreateView.as_view(), name='calificacion_create'),
    path('<int:pk>/editar/',    CalificacionUpdateView.as_view(), name='calificacion_update'),
    path('<int:pk>/eliminar/',  CalificacionDeleteView.as_view(), name='calificacion_delete'),
    path('estudiante/',         CalificacionEstudianteView.as_view(), name='calificacion_estudiante'),
    path('estudiante/<int:pk>/',CalificacionEstudianteView.as_view(), name='calificacion_estudiante_detail'),
]
```

### ¿Qué es `<int:pk>`?

Es un **parámetro de URL**. Captura el número de la URL y lo pasa a la vista.

```
URL: /calificaciones/5/editar/
                     ^ pk = 5
```

La vista accede a él con `self.kwargs['pk']` o automáticamente a través de `get_object()`.

### Cómo se encadenan las URLs

```python
# aulatec/urls.py (raíz)
path('', include('gestion_aulatec.urls'))

# gestion_aulatec/urls/__init__.py
path('calificaciones/', include('gestion_aulatec.urls.CalificacionUrls'))

# CalificacionUrls.py
path('nuevo/', CalificacionCreateView.as_view(), name='calificacion_create')

# URL final completa:
# /calificaciones/nuevo/
```

---

## 10. El Middleware

Un **middleware** es una clase que se ejecuta **en cada petición** antes de llegar a la vista y en cada respuesta antes de salir al navegador.

```python
# gestion_aulatec/middleware.py

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # la siguiente capa

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return self.get_response(request)  # admin → pasa libre

            path_cambio = reverse('gestion_aulatec:cambiar_password')
            path_logout = reverse('gestion_aulatec:logout')

            if request.user.debe_cambiar_password:
                # Si no está en la página de cambio ni en logout → redirige
                if request.path != path_cambio and request.path != path_logout:
                    return redirect(path_cambio)

        return self.get_response(request)  # continúa normalmente
```

### ¿Cómo se registra el middleware?

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    ...
    'gestion_aulatec.middleware.ForcePasswordChangeMiddleware',  # el nuestro
]
```

El orden importa — se ejecutan de arriba a abajo en cada petición.

---

## 11. Autenticación y Sesiones

### Usuario personalizado

AulaTec no usa el modelo de usuario por defecto de Django — usa uno propio:

```python
class Usuario(AbstractBaseUser, PermissionsMixin):
    NumId = models.CharField(max_length=10, unique=True)
    Rol   = models.CharField(max_length=50)
    debe_cambiar_password = models.BooleanField(default=True)

    USERNAME_FIELD = 'NumId'  # ← se loguea con el número de doc, no con email
```

```python
# settings.py
AUTH_USER_MODEL = 'gestion_aulatec.Usuario'
```

### Flujo de login

```python
def login_view(request):
    if request.method == 'POST':
        NumId    = form.cleaned_data['NumId']
        password = form.cleaned_data['password']

        user = authenticate(request, username=NumId, password=password)
        # authenticate busca el usuario en BD y verifica la contraseña (hash)

        if user is not None:
            login(request, user)  # crea la sesión en el servidor
            if user.Rol == 'Administrador':
                return redirect('gestion_aulatec:admin_dashboard')
            elif user.Rol == 'Docente':
                return redirect('gestion_aulatec:docente_dashboard')
            elif user.Rol == 'Estudiante':
                return redirect('gestion_aulatec:estudiante_dashboard')
```

### ¿Cómo funciona la sesión?

1. Al hacer `login(request, user)`, Django guarda el ID del usuario en la base de datos (tabla `django_session`)
2. Le envía al navegador una **cookie** llamada `sessionid`
3. En cada petición siguiente, el navegador manda esa cookie
4. Django la lee, busca el usuario y lo pone en `request.user`
5. Al hacer `logout()`, Django borra la sesión de la BD y la cookie

La sesión en AulaTec expira a los **30 minutos de inactividad** (`SESSION_COOKIE_AGE = 1800`).

---

## 12. CSRF — Protección de formularios

**CSRF** (Cross-Site Request Forgery) es un ataque donde un sitio malicioso hace que el navegador de la víctima envíe peticiones no autorizadas a tu aplicación.

Django lo previene con un **token secreto** que incluye en cada formulario:

```html
<form method="POST">
    {% csrf_token %}   ← genera un campo oculto con un token único
    ...
</form>
```

Si el POST no incluye el token válido, Django lo rechaza con error 403. Por eso todos los formularios del proyecto tienen `{% csrf_token %}`.

---

## 13. Señales de alerta — preguntas difíciles

### "¿Qué diferencia hay entre MVT y MVC?"

En MVC clásico el **Controller** recibe la petición y coordina todo.
En MVT de Django esa responsabilidad se divide:
- La **URL** actúa como el enrutador (parte del controller)
- La **View** procesa la lógica (parte del controller)
- El **Template** genera la presentación (la V de MVC)
- El **Model** es igual en ambos patrones

### "¿Qué pasa si dos usuarios guardan la misma calificación al mismo tiempo?"

El `unique_together` en el modelo genera una restricción en la base de datos. Aunque dos peticiones lleguen simultáneamente, la BD garantiza que solo una podrá insertar — la segunda recibirá un `IntegrityError` que el sistema maneja mostrando un error de validación.

### "¿Por qué usan CBV y no funciones (FBV)?"

Las CBV evitan repetir código. `CreateView`, `UpdateView` y `DeleteView` ya implementan internamente el flujo GET/POST, la validación del formulario y la redirección. Nosotros solo sobreescribimos lo que necesita lógica personalizada.

### "¿Qué es `select_related`?"

```python
Calificacion.objects.select_related('IdEstudiante__IdUsuario', 'IdMateria')
```

Optimización del ORM. Sin ella, acceder a `cal.IdEstudiante.IdUsuario.Nombres` genera una consulta SQL separada por cada calificación (problema N+1). Con `select_related`, Django hace un solo JOIN y trae todo de una vez.

### "¿Cómo garantizan que la matrícula no quede a medias?"

Con una **transacción atómica**:

```python
with transaction.atomic():
    # 1. Crear usuario
    # 2. Crear estudiante
    # 3. Crear acudiente
    # 4. Crear matrícula
    # Si cualquier paso lanza una excepción, todo se revierte
```

`atomic()` envuelve todas las operaciones en una transacción SQL. Si algo falla en el paso 3, los pasos 1 y 2 también se deshacen automáticamente.

---

## 14. Estructura completa del proyecto

```
Proyec-AulaTec/
├── aulatec/                    ← configuración del proyecto Django
│   ├── settings.py             ← configuración general
│   ├── settings_local.py       ← configuración local (MariaDB, no se sube a git)
│   └── urls.py                 ← URLs raíz
│
├── gestion_aulatec/            ← app principal
│   ├── models/                 ← tablas de la BD (una clase = una tabla)
│   │   ├── usuario.py
│   │   ├── estudiante.py
│   │   ├── docente.py
│   │   ├── grado.py
│   │   ├── materia.py
│   │   ├── horario.py
│   │   ├── matricula.py
│   │   ├── acudiente.py
│   │   ├── calificacion.py     ← tu módulo
│   │   └── certificado.py
│   │
│   ├── views/                  ← lógica de cada módulo
│   │   ├── LoginViews.py       ← login, logout, dashboards
│   │   ├── calificacion_views.py  ← tu módulo
│   │   └── ...
│   │
│   ├── forms/                  ← formularios con validación
│   │   ├── CalificacionForm.py ← tu módulo
│   │   └── ...
│   │
│   ├── urls/                   ← enrutamiento por módulo
│   │   ├── CalificacionUrls.py ← tu módulo
│   │   └── ...
│   │
│   ├── templates/              ← archivos HTML
│   │   └── gestion_aulatec/
│   │       ├── calificacion_list.html
│   │       ├── calificacion_form.html
│   │       └── ...
│   │
│   ├── static/css/             ← estilos CSS
│   ├── middleware.py           ← control de cambio de contraseña
│   └── migrations/             ← historial de cambios en la BD
│
└── docs/                       ← esta carpeta
    ├── demo_presentacion.md
    └── conceptos_tecnicos.md
```

---

## 15. Resumen rápido para el día de la presentación

| Concepto | Definición en una línea |
|---|---|
| Django | Framework web de Python con todo incluido |
| MVT | Patrón de arquitectura: Model (datos), View (lógica), Template (HTML) |
| Model | Clase Python que representa una tabla en la BD |
| ORM | Sistema que traduce Python a SQL automáticamente |
| QuerySet | Resultado de una consulta ORM, evaluación lazy |
| ForeignKey | Relación entre dos tablas (apunta a un registro de otra tabla) |
| View (CBV) | Clase que recibe petición HTTP, consulta modelo, devuelve respuesta |
| Template | HTML con variables y etiquetas Django para mostrar datos dinámicos |
| Form | Clase que define campos de formulario y sus validaciones |
| Middleware | Capa que intercepta cada petición antes de llegar a la vista |
| Sesión | Mecanismo para recordar al usuario entre peticiones |
| CSRF | Protección contra formularios enviados desde sitios externos |
| Mixin | Clase auxiliar que añade comportamiento a una vista |
| Migración | Registro de un cambio en la estructura de la BD |
| `unique_together` | Restricción que impide duplicados por combinación de campos |
| `transaction.atomic` | Garantiza que todas las operaciones se guardan o ninguna |
