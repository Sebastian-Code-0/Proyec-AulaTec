# AulaTec

AulaTec es una plataforma desarrollada en **Django** para la gestión académica.

## Tecnologías utilizadas
- Python 3
- Django
- MySQL (desarrollo) (despliegue)
- GitHub

## Estructura del repositorio
- `aulatec/` → Configuración principal de Django  
- `gestion_aulatec/` → Aplicaciones del proyecto  
- `MySQL` → Base de datos usada en desarrollo  
- `database/aulatec.sql` → Script de la base de datos (exportado)

## Instalación y ejecución
1. Clonar el repositorio:
   ```bash
   https://github.com/Kevinvalderrama-23/AulaTec
   cd AulaTec

## Despliegue del proyecto (Crear entorno virtual e instalar dependencias)
2. python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

## Configurar la base de datos
Si usas MySQL, importa el script que está en database/aulatec.sql.

## Ejecución
python manage.py runserver

## Autores
- Kevin Valderrama
- Sebastian Valencia
- leidy
- Alejandro
