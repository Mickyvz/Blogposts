import re

from flask import Blueprint, render_template, request

from .models import Post, User

bp = Blueprint('home', __name__)

def get_user(id):
    user = User.query.get_or_404(id)
    return user

def search_posts(query):
    posts = Post.query.filter(Post.title.ilike(f'%{query}%')).all()
    return posts

def reading_time(html):
    """Estima los minutos de lectura de un contenido HTML (~200 palabras/min)."""
    text = re.sub('<[^<]+?>', ' ', html or '')
    words = len(text.split())
    return max(1, round(words / 200))

@bp.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()
    if request.method == 'POST':
        query = request.form.get('search')
        posts = search_posts(query)
        value = 'hidden'
        return render_template('index.html', posts=posts, get_user=get_user, value=value)
    return render_template('index.html', posts=posts, get_user=get_user)


@bp.route('/blog/<url>')
def blog(url):
    post = Post.query.filter_by(url=url).first_or_404()
    return render_template('blog.html', post=post, get_user=get_user, reading_time=reading_time(post.content))
