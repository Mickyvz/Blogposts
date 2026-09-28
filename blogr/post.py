from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, abort

from .auth import login_required
from .models import Post
from .slugify import slugify
from blogr import db


def unique_post_url(title, exclude_id=None):
    """Genera un slug a partir del título del post y le añade un sufijo
    -2, -3, ... si ya existe, hasta encontrar uno libre."""
    base = slugify(title)[:196]
    url = base
    suffix = 2
    while True:
        query = Post.query.filter_by(url=url)
        if exclude_id is not None:
            query = query.filter(Post.id != exclude_id)
        if query.first() is None:
            return url
        url = f"{base}-{suffix}"
        suffix += 1

bp = Blueprint("post", __name__, url_prefix="/post")


def get_owned_post(id):
    post = Post.query.get_or_404(id)
    if post.author != g.user.id:
        abort(403)
    return post


@bp.route("/posts")
@login_required
def posts():
    posts = Post.query.filter_by(author=g.user.id).order_by(Post.created.desc()).all()

    return render_template('admin/posts.html', posts=posts)


@bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        info = request.form.get('info')
        content = request.form.get('ckeditor')

        url = unique_post_url(title)
        post = Post(g.user.id, url, title, info, content)

        db.session.add(post)
        db.session.commit()
        flash(f'El blog {post.title} ha sido creado exitosamente')
        return redirect(url_for('post.posts'))
    return render_template('admin/create.html')


@bp.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update(id):
    post = get_owned_post(id)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.info = request.form.get('info')
        post.content = request.form.get('ckeditor')

        db.session.commit()
        flash(f'El blog {post.title} ha sido actualizado exitosamente')
        return redirect(url_for('post.posts'))
    return render_template('admin/update.html', post=post)


@bp.route("/delete/<int:id>", methods=['POST'])
@login_required
def delete(id):
    post = get_owned_post(id)
    title = post.title
    db.session.delete(post)
    db.session.commit()
    flash(f'El blog {title} ha sido eliminado exitosamente')
    return redirect(url_for('post.posts'))
