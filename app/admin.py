import json
from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app as app, render_template, flash, request, redirect, url_for
from playhouse.flask_utils import get_object_or_404
from werkzeug.security import safe_join

from .models import Article
from . import forms
from .auth import auth


admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates/admin')


@admin.get('/')
@auth.login_required
def index():
    articles = Article.select().order_by(Article.created_at.desc())
    return render_template('home.html', articles=articles)


@admin.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create_article():
    form = forms.EditorForm()

    if request.method == 'POST' and form.validate_on_submit():
        article = Article.create(**form.data)
        flash('Статья опубликована', 'success')
        return redirect(url_for('admin.edit_article', id=article.id))

    return render_template('editor.html', form=form)


@admin.route('/edit/<id>', methods=('GET', 'POST'))
@auth.login_required
def edit_article(id):
    article = get_object_or_404(Article, (Article.id == id))
    form = forms.EditorForm(obj=article)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(article)
        article.updated_at = datetime.now().replace(microsecond=0)
        article.save()
        flash('Статья сохранена', 'success')

    return render_template('editor.html', article=article, form=form)


@admin.route('/delete/<id>')
@auth.login_required
def delete_article(id):
    article = get_object_or_404(Article, (Article.id == id))
    article.delete_instance()
    flash(f'Статья "{article.title}" удалена', 'success')
    return redirect(url_for('admin.index'))


@admin.route('/settings', methods=('GET', 'POST'))
@auth.login_required
def settings():
    settings_path = Path(app.instance_path, 'settings.json')

    if not settings_path.exists():
        with open(settings_path, 'w+') as file:
            file.write('{}')

    with open(settings_path, 'r+') as file:
        settings_data = json.load(file)

    form = forms.SettingsForm(data=settings_data)

    if request.method == 'POST' and form.validate_on_submit():
        data = form.data
        data.pop('csrf_token')
        data.pop('submit')

        with open(settings_path, 'w+') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    return render_template('settings.html', form=form)
