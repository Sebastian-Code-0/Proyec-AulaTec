# 🎓 AulaTec
 
**Academic management system for schools — built with Django.**
 
AulaTec is a web platform designed to streamline school administration. It provides tools for managing students, teachers, courses, schedules, grades, and certificates — while giving parents and students real-time access to academic information without waiting for physical report cards.
 
---
 
### 🇨🇴 Español
 
AulaTec es una plataforma web diseñada para facilitar la administración escolar. Ofrece herramientas para gestionar estudiantes, profesores, cursos, horarios, calificaciones y certificados — brindanda a padres y estudiantes acceso en tiempo real a la información académica sin tener que esperar por un boletín físico.
 
---
 
### Features / Funcionalidades
 
- Student & teacher management / Gestión de estudiantes y profesores
- Course & schedule management / Gestión de cursos y horarios
- Grade tracking & academic progress reports / Seguimiento de notas e informes de progreso académico
- Certificate generation / Generación de certificados
- Email notifications / Notificaciones por correo electrónico
- Parent access to student info / Acceso de padres a la información del estudiante
### Tech Stack
 
```
Backend:     Python · Django
Frontend:    HTML · CSS · JavaScript
Database:    MySQL
```
 
### Getting Started / Instalación
 
**1. Clone the repo / Clonar el repositorio:**
 
```bash
git clone https://github.com/Sebastian-Code-0/AulaTec.git
cd AulaTec
```
 
**2. Create virtual environment / Crear entorno virtual:**
 
```bash
python -m venv env
source env/bin/activate        # Linux / Mac
env\Scripts\activate           # Windows
```
 
**3. Install dependencies / Instalar dependencias:**
 
```bash
pip install -r requirements.txt
```
 
**4. Set up the database / Configurar la base de datos:**
 
Import the SQL script located in `database/aulatec.sql` into your MySQL server.
 
Importa el script SQL ubicado en `database/aulatec.sql` en tu servidor MySQL.
 
**5. Run the server / Ejecutar el servidor:**
 
```bash
python manage.py migrate
python manage.py runserver
```
 
### Project Structure / Estructura del proyecto
 
```
AulaTec/
├── aulatec/            # Django project settings / Configuración del proyecto
├── gestion_aulatec/    # Main app (views, models, forms) / App principal
├── manage.py
└── requirements.txt
```
 
### Authors / Autores
 
- Sebastian Valencia
- Kevin Andrés Valderrama Lozano
- Leidy Alejandra Pechene Sanabria
- Alejandro Ramírez Quiscue

### License / Licencia

All rights reserved. / Todos los derechos reservados.
