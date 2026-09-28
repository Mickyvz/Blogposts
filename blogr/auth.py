import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, abort, current_app

from werkzeug.security import check_password_hash, generate_password_hash

from .models import User

from blogr import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

MIN_PASSWORD_LENGTH = 6
ALLOWED_PHOTO_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

@bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password') or ''

        # Validación de datos
        error = None

        if not username or not email:
            error = "El nombre de usuario y el correo son obligatorios"
        elif len(password) < MIN_PASSWORD_LENGTH:
            error = f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres"
        elif User.query.filter_by(email=email).first() is not None:
            error = f"El correo {email} ya está registrado"

        if error is None:
            user = User(username, email, generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)
        
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validación de datos
        error = None

        user = User.query.filter_by(email=email).first()

        if user == None or not check_password_hash(user.password, password):
            error = "Usuario o contraseña incorrectos"

        # Iniciando sesión
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('post.posts'))
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = db.session.get(User, user_id) if user_id is not None else None

    if user_id is not None and g.user is None:
        session.clear()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))

import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# editar perfil
from werkzeug.utils import secure_filename


def save_profile_photo(photo, user_id):
    extension = secure_filename(photo.filename).rsplit('.', 1)[-1].lower()
    if extension not in ALLOWED_PHOTO_EXTENSIONS:
        return None

    filename = f'user{user_id}-{uuid.uuid4().hex[:8]}.{extension}'
    media_dir = os.path.join(current_app.root_path, 'static', 'media')
    os.makedirs(media_dir, exist_ok=True)
    photo.save(os.path.join(media_dir, filename))
    return f'media/{filename}'


@bp.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    if id != g.user.id:
        abort(403)

    user = g.user

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') or ''
        photo = request.files.get('photo')

        error = None
        if not username:
            error = "El nombre de usuario es obligatorio"
        elif password and len(password) < MIN_PASSWORD_LENGTH:
            error = f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres"

        photo_path = None
        if error is None and photo and photo.filename:
            photo_path = save_profile_photo(photo, user.id)
            if photo_path is None:
                error = "La foto debe ser PNG, JPG, GIF o WEBP"

        if error is None:
            user.username = username
            if password:
                user.password = generate_password_hash(password)
            if photo_path:
                user.photo = photo_path
            db.session.commit()
            return redirect(url_for('auth.profile', id=user.id))

        flash(error)

    return render_template('auth/profile.html', user=user)

