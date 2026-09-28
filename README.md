# BlogPosts

Aplicación web de blogs construida con Flask, donde los usuarios pueden registrarse, publicar artículos con un editor enriquecido y gestionar su perfil. El diseño visual es un sistema propio inspirado en la estética "ledger" de Modern Treasury: papel blanco, tinta oscura, tipografía monoespaciada para metadatos y acentos verdes.

## Funcionalidades

- Registro e inicio de sesión de usuarios, con contraseñas hasheadas y validación de formularios
- Creación, edición y eliminación de blogs propios, con control de propiedad (un usuario no puede editar el post de otro)
- Editor de texto enriquecido (CKEditor) para el contenido de los artículos
- Generación automática de URLs amigables a partir del título (con manejo de colisiones)
- Sanitización de HTML del contenido publicado (protección contra XSS) con `bleach`
- Protección CSRF en todos los formularios
- Buscador de artículos por título
- Estimación de tiempo de lectura por artículo
- Perfil de usuario editable, incluyendo foto de perfil
- Diseño responsivo propio, con animaciones de entrada y scroll

## Stack técnico

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-WTF (CSRF)
- **Base de datos:** PostgreSQL
- **Frontend:** Jinja2, CSS propio (sin frameworks de diseño), Bootstrap solo como base estructural puntual, JavaScript vanilla para animaciones
- **Editor de contenido:** Flask-CKEditor
- **Seguridad:** sanitización de HTML con `bleach`, protección CSRF, hashing de contraseñas

## Estructura del proyecto

```
blogr/
├── auth.py            # Registro, login, perfil de usuario
├── home.py             # Portada y vista de blog individual
├── post.py             # Crear, editar, eliminar y listar blogs propios
├── models.py           # Modelos User y Post (SQLAlchemy)
├── sanitize.py          # Filtro Jinja para limpiar HTML
├── slugify.py           # Generación de slugs para URLs
├── static/
│   ├── css/theme.css    # Sistema de diseño (tokens, componentes)
│   └── img/
└── templates/
    ├── admin/            # Crear/editar/listar blogs
    ├── auth/             # Login, registro, perfil
    └── index.html, blog.html, base.html
```

## Ejecutar en local

```bash
python -m venv env-blog
env-blog\Scripts\activate       # Windows
pip install -r requirements.txt

# Variables de entorno necesarias
set SECRET_KEY=una-clave-aleatoria
set DATABASE_URL=postgresql://usuario:password@localhost/blogpost_db

python run.py
```

La aplicación crea las tablas automáticamente al iniciar (`db.create_all()`), sobre una base de datos PostgreSQL ya existente.
