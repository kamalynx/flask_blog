from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class EditorForm(FlaskForm):
    title = StringField('Заголовок', validators=(DataRequired(),))
    description = TextAreaField('Описание')
    slug = StringField('URI', validators=(DataRequired(),))
    content = TextAreaField('Содержимое')
    submit = SubmitField('Сохранить')


class SettingsForm(FlaskForm):
    title = StringField('Название сайта', validators=(DataRequired(),))
    description = TextAreaField('Описание сайта')
    submit = SubmitField('Сохранить')
