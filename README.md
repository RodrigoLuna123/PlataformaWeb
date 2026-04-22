# 🎓 Plataforma de Gestión Escolar - Django & SQL Server

Sistema integral para la administración académica, diseñado con un enfoque en la seguridad de datos y la eficiencia administrativa.

## 🚀 Características Principales
* **Panel de Administrador:** Gestión total de alumnos, inscripciones y reportes de demanda en PDF.
* **Módulo de Profesor:** Publicación de actividades, centro de calificaciones masivo y sistema de notificaciones.
* **Interfaz de Alumno:** Visualización de contenidos, calendario de entregas y seguimiento de notas.
* **Seguridad Avanzada:** Implementación de cifrado AES-256 para documentos sensibles y borrado en cascada en SQL Server.

## 🛠️ Tecnologías Utilizadas
* **Backend:** Django 5.x / Python 3.13
* **Base de Datos:** Microsoft SQL Server
* **Frontend:** Bootstrap 5 (Diseño responsivo estilo Blackboard)
* **Reportes:** ReportLab / WeasyPrint (Generación de PDFs)

## 🔧 Configuración
1. Clona el repositorio.
2. Instala las dependencias: `pip install -r requirements.txt`.
3. Configura la conexión a tu instancia de SQL Server en `settings.py`.
4. Ejecuta `python manage.py runserver`.