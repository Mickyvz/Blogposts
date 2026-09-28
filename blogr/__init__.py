from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__)

    # Configurar la aplicación
    app.config.from_object('config.Config')

    db.init_app(app)
    csrf.init_app(app)

    from flask_ckeditor import CKEditor
    ckeditor = CKEditor(app)

    from .sanitize import clean_html
    app.jinja_env.filters['clean_html'] = clean_html

    from datetime import datetime

    @app.context_processor
    def inject_year():
        return {'now_year': datetime.now().year}

    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES')


    # registrar vistas
    
    from blogr import home
    app.register_blueprint(home.bp)

    from blogr import auth
    app.register_blueprint(auth.bp)

    from blogr import post
    app.register_blueprint(post.bp)

    from .models import User, Post

    with app.app_context():
        db.create_all()


    return app