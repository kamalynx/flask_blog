from flask import Blueprint, render_template, request, jsonify
from playhouse.flask_utils import get_object_or_404

from .models import Article
from .auth import auth


api = Blueprint('api', __name__, template_folder='templates', url_prefix='/api')

@api.post('/create')
@auth.login_required
def create_article():
    article = Article.create(**request.get_json())
    return jsonify({'status': 'ok'}), 201


@api.delete('/delete/<id>')
@auth.login_required
def delete_article(id: int):
    article = get_object_or_404(Article, (Article.id == id))
    article.delete_instance()
    return '', 204


@api.post('/update/<id>')
@auth.login_required
def update_article(id):
    article = get_object_or_404(Article, (Article.id == id))
    article.update(**request.get_json()).execute()
    return jsonify({'status': 'updated'}), 200
