from flask import current_app as app, render_template, send_from_directory, request, jsonify
from playhouse.flask_utils import get_object_or_404
from werkzeug.security import safe_join
from flask_caching import Cache

from .models import Article


cache = Cache(app)


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.get('/')
@cache.cached()
def index():
    articles = Article.select().order_by(Article.created_at.desc())
    return render_template('index.html', articles=articles)


@app.get('/<slug>', endpoint='article')
@cache.cached()
def get_article(slug):
    article = get_object_or_404(Article, (Article.slug == slug))
    return render_template('single.html', article=article)


@app.get('/favicon.ico')
def favicon():
    return send_from_directory(app.instance_path, 'favicon.ico')


@app.get('/images/<filename>')
def send_file(filename):
    return send_from_directory(safe_join(app.instance_path, 'images'), filename)
