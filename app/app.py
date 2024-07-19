from pathlib import Path
import json
import locale

from flask import Flask
from flask_minify import Minify


def create_app():
    locale.setlocale(locale.LC_ALL, '')


    BASE_DIR = Path().resolve()
    DATA_DIR = BASE_DIR / 'data'

    if not DATA_DIR.exists():
        DATA_DIR.mkdir()

    app = Flask(__name__, instance_path=DATA_DIR)
    app.config['DATABASE_URL'] = f'sqlite:///{DATA_DIR}/db.sqlite3'
    app.config['CACHE_TYPE'] = 'SimpleCache'
    # ~ app.config['DATABASE_URL'] = 'postgresql://blog:blog@localhost:5433/blog'
    app.config.from_pyfile(DATA_DIR / 'config.py', silent=True)


    with app.app_context():
        from . import models, views
        from .api import api
        from .admin import admin

        models.db.database.create_tables((models.Article,))

    app.register_blueprint(api)
    app.register_blueprint(admin)

    @app.context_processor
    def load_site_settings():
        settings = {}

        try:
            with open(DATA_DIR / 'settings.json') as file:
                settings.update(json.load(file))
            return settings
        except FileNotFoundError as err:
            app.logger.error(err)

        return settings

    Minify(app, go=True)

    return app
