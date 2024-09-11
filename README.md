# Newspaper - Periódico Digital

![Django](https://img.shields.io/badge/Django-4.0+-success?style=flat-square&logo=django)
![SQLite](https://img.shields.io/badge/SQLite-3.x-blue?style=flat-square&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-purple?style=flat-square&logo=bootstrap)
![Python](https://img.shields.io/badge/Python-3.x-yellow?style=flat-square&logo=python)

## Descripción del Proyecto
El **Periódico Digital** es una plataforma web donde los usuarios pueden acceder a artículos de noticias, dejando comentarios y participando activamente. El proyecto está diseñado con diferentes roles de usuarios, permitiendo una gestión organizada del contenido y el acceso.

### Roles de usuarios:
- **Super Usuario**: Control total sobre el sistema, acceso a todas las funcionalidades y la administración de la plataforma.
- **Editores**: Pueden crear, editar y publicar artículos.
- **Lectores**: Tienen acceso a leer artículos y pueden comentar en ellos una vez que se hayan autenticado.

### Tecnologías utilizadas:
- **Frontend**: HTML, CSS, JavaScript y Bootstrap.
- **Backend**: Django (con SQLite como base de datos).
- **Base de Datos**: SQLite.

Este proyecto se centra principalmente en la práctica del framework Django, implementando sus modelos, vistas, autenticación y permisos, mientras que el frontend es más simple en comparación, utilizando componentes básicos de Bootstrap.

---

## Funcionalidades
- 🔐 **Autenticación de usuarios**: Registro e inicio de sesión.
- 📰 **Gestión de artículos**: Creación, edición y filtrado por categorías y etiquetas.
- 💬 **Comentarios en artículos**: Los lectores pueden comentar en los artículos tras iniciar sesión.
- 👥 **Roles de usuario**: Diferentes permisos de acceso según el rol.
- 🔍 **Búsqueda de artículos**: Filtros por categorías y etiquetas.

---

## Requisitos

- **Python** 3.x
- **Django** 4.x
- **SQLite** (incluido en Django por defecto)
- **pip** (para instalar dependencias)

---


## Instalación

### Clonar el repositorio:
```bash
git clone https://github.com/usuario/newspaper.git
cd newspaper```

### Crear un entorno virtual:
```bash
python -m venv env
source env/bin/activate  # Para Linux y Mac
env\Scripts\activate```  # Para Windows

### Migrar la base de datos:
```bash
python manage.py migrate```

### Crear un superusuario:
```bash
python manage.py createsuperuser```

### Iniciar el Servidor
```bash
python manage.py runserver```

## Cómo agregar editores y usuarios de staff

Para agregar usuarios como editores (staff), puedes hacerlo desde la consola de Django:

### Accede a la shell de Django:
```bash
python manage.py shell```
```python
from django.contrib.auth.models import User
user = User.objects.get(username='nombre_de_usuario')
user.is_staff = True  # Asigna como staff
user.save()
```
---

## Posibles mejoras futuras
- 🔍 Implementar búsqueda avanzada por artículos.
- 🌐 Soporte para múltiples idiomas.
- 📧 Añadir notificaciones por email para los comentarios en los artículos.
- 📱 Diseño responsivo avanzado para móviles.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas colaborar, por favor abre un issue o envía un pull request en el repositorio.

## Licencia
Este proyecto está bajo la [Licencia MIT](https://opensource.org/licenses/MIT).





