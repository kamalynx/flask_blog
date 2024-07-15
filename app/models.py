from datetime import datetime

from flask import current_app
from markdown import markdown
from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    TextField,
)
from playhouse.flask_utils import FlaskDB


db = FlaskDB(current_app)


class Article(db.Model):
    id = AutoField()
    title = CharField(verbose_name='Заголовок')
    description = CharField(max_length=255, verbose_name='Описание', default='')
    slug = CharField(max_length=255, unique=True, index=True)
    content = TextField(verbose_name='Содержимое', default='')
    image = CharField(max_length=255, verbose_name='Изображение', help_text='URL адрес картинки', default='')
    created_at = DateTimeField(default=datetime.now().replace(microsecond=0))
    updated_at = DateTimeField(default=datetime.now().replace(microsecond=0))

    def __str__(self):
        return self.title

    @property
    def content_as_markdown(self):
        return markdown(self.content, extensions=('pymdownx.tilde', 'codehilite', 'extra'))

    @property
    def date_creation(self):
        return self.created_at.strftime('%d %B %Y')
