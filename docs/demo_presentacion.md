# Script de Demo — AulaTec
### Presentación Final

> **Tiempo estimado:** 15–20 minutos  
> **Antes de empezar:** servidor corriendo, navegador abierto en `http://127.0.0.1:8000`, base de datos con datos reales.

---

## Preparación previa (hacer antes de entrar al salón)

- [ ] Servidor Django corriendo: `python manage.py runserver`
- [ ] Navegador abierto en la home: `http://127.0.0.1:8000`
- [ ] Cerrar sesión si quedó alguna activa
- [ ] Tener a mano las credenciales de prueba (ver abajo)
- [ ] Cerrar pestañas innecesarias

**Credenciales listas:**
| Rol | NumId | Contraseña |
|---|---|---|
| Administrador | 1033700796 | Stab161022 |
| Docente | 100 | (la que tengas) |
| Estudiante | 1000000000 | (la que tengas) |

---

## BLOQUE 1 — Home pública (1 min)

**Acción:** Mostrar la pantalla de inicio sin iniciar sesión.

**Qué decir:**
> "Esta es la pantalla principal de AulaTec. Es pública — cualquiera puede verla. Muestra estadísticas generales de la institución: total de estudiantes, docentes, matrículas y grados registrados. Estos datos vienen directamente de la base de datos en tiempo real."

**Qué señalar:** Los contadores de estadísticas.

---

## BLOQUE 2 — Login y redirección por rol (1 min)

**Acción:** Hacer login como Administrador.

**Qué decir:**
> "El sistema no usa nombre de usuario ni correo para ingresar — usa el número de identificación del usuario. Esto es una decisión de diseño adaptada al contexto colombiano donde todos tienen cédula o tarjeta de identidad. Dependiendo del rol, el sistema redirige automáticamente al panel correspondiente."

**Qué señalar:** Que al ingresar va directo al dashboard de admin, no a una pantalla genérica.

---

## BLOQUE 3 — Dashboard Administrador (2 min)

**Acción:** Mostrar el dashboard del administrador.

**Qué decir:**
> "El administrador tiene visibilidad total del sistema. En su panel ve un resumen: estudiantes activos, docentes, matrículas del año en curso, materias, horarios activos y certificados pendientes de aprobación. Todo actualizado en tiempo real."

**Qué señalar:** Los contadores del dashboard, especialmente matrículas del año actual.

---

## BLOQUE 4 — Crear Matrícula (4 min) ⭐ punto fuerte

**Acción:** Ir a Matrículas → Nueva Matrícula y llenar el formulario en vivo.

**Datos sugeridos para usar en demo:**
```
Estudiante:
  Tipo doc: TI
  Número: 20242025
  Nombres: Demo
  Apellidos: Presentacion
  Email: demo@aulatec.com
  Celular: 3001234567

Grado: (cualquiera)
Año lectivo: 2026
Colegio anterior: Colegio Demo
Fecha nacimiento: 2010-01-15
Lugar nacimiento: Bogotá D.C.
Barrio: Centro
EPS: Sura
Condición médica: No
Último grado: 5°
Institución anterior: Escuela Demo
Ciudad institución: Bogotá D.C.
Repite grado: No
Apoyo pedagógico: No
Autoriza datos: ✓ (obligatorio)

Acudiente:
  Tipo: CC
  Número: 99887766
  Nombres: Padre Demo
  Apellidos: Acudiente
  Celular: 3109876543
  Parentesco: Padre
```

**Qué decir mientras llenas:**
> "El formulario de matrícula captura toda la información requerida por la institución. Al guardar, el sistema hace varias cosas en una sola operación atómica: crea el usuario del estudiante con contraseña generada automáticamente, crea el perfil de estudiante, registra al acudiente y genera el número de matrícula. Si cualquier paso falla, se revierte todo — no quedan datos a medias."

**Después de guardar, señalar:**
> "El sistema envió automáticamente un correo al estudiante con sus credenciales de acceso. Y aquí podemos ver la matrícula creada en la lista."

---

## BLOQUE 5 — Verificar usuario creado (1 min)

**Acción:** Ir a Usuarios y buscar el estudiante recién creado.

**Qué decir:**
> "Podemos verificar que el sistema creó correctamente el usuario con rol Estudiante. Al primer ingreso, el sistema le pedirá obligatoriamente que cambie su contraseña — eso es una medida de seguridad implementada con un middleware personalizado."

---

## BLOQUE 6 — Exportar Excel (30 seg)

**Acción:** En la lista de matrículas, hacer clic en Exportar Excel.

**Qué decir:**
> "El administrador puede exportar todas las matrículas activas del año a un archivo Excel con formato institucional — encabezados, colores, agrupaciones por secciones y totales automáticos."

---

## BLOQUE 7 — Login como Docente (3 min)

**Acción:** Cerrar sesión, ingresar como docente.

**Qué decir:**
> "El docente tiene un panel completamente diferente. Solo ve su información: las materias que tiene asignadas, sus horarios activos y las últimas calificaciones que registró."

**Registrar una calificación:**
> "Aquí el docente registra una calificación. El sistema solo le muestra sus propios estudiantes y sus propias materias — no puede ver ni modificar datos de otros docentes. El año lectivo se asigna automáticamente. Y si intenta registrar la misma actividad dos veces para el mismo estudiante, el sistema lo bloquea."

**Qué señalar:** Que el campo docente está preseleccionado y bloqueado — no puede asignársela a otro.

---

## BLOQUE 8 — Login como Estudiante (3 min)

**Acción:** Cerrar sesión, ingresar con el estudiante nuevo creado en el bloque 4.

**Qué decir:**
> "Al ingresar por primera vez, el sistema intercepta la navegación y obliga al estudiante a cambiar su contraseña antes de poder hacer cualquier otra cosa. Esto lo hace un middleware — una capa de seguridad que revisa cada petición."

**Cambiar contraseña, luego mostrar:**
> "Una vez cambiada, el estudiante accede a su panel personal. Ve sus calificaciones con promedios por período, su horario de clases y puede solicitar certificados."

**Solicitar certificado:**
> "El estudiante solicita un certificado, queda en estado pendiente, y el administrador debe aprobarlo. Una vez aprobado, el estudiante puede descargar el PDF. El certificado tiene una vigencia de 30 días."

---

## BLOQUE 9 — Aprobar certificado (1 min)

**Acción:** Volver al admin y aprobar el certificado.

**Qué decir:**
> "El administrador ve la solicitud pendiente en su panel. La aprueba, el sistema genera el código único del certificado y registra quién lo aprobó y cuándo."

---

## Cierre (30 seg)

**Qué decir:**
> "En resumen, AulaTec es un sistema web completo que digitaliza la gestión académica de una institución. Implementa autenticación personalizada, control de acceso por roles, generación de documentos PDF, exportación a Excel y comunicación por correo electrónico, todo construido con Django siguiendo el patrón MVT."

---

## Preguntas frecuentes — respuestas preparadas

**¿Por qué Django?**
> "Django es un framework de alto nivel para Python que incluye ORM, sistema de autenticación, manejo de sesiones y protección contra vulnerabilidades comunes como CSRF e inyección SQL — todo integrado. Nos permitió enfocarnos en la lógica del negocio."

**¿Qué base de datos usan?**
> "MariaDB, que es compatible con MySQL. La conectamos mediante la librería `mysqlclient`. Django abstrae la base de datos con su ORM, por lo que cambiar de motor requeriría solo modificar la configuración."

**¿Cómo manejan la seguridad de las contraseñas?**
> "Django nunca guarda contraseñas en texto plano. Usa el algoritmo PBKDF2 con SHA256 y sal aleatoria por defecto. Nosotros además forzamos el cambio en el primer ingreso."

**¿Qué es el middleware que mencionaron?**
> "Es una clase que se ejecuta en cada petición HTTP antes de llegar a la vista. El nuestro revisa si el usuario debe cambiar su contraseña y, si es así, lo redirige independientemente de la URL que haya pedido."

**¿Cómo protegen las rutas?**
> "Con mixins de Django: `LoginRequiredMixin` verifica que haya sesión activa, y `UserPassesTestMixin` verifica que el rol del usuario coincida con el permitido para esa vista."
