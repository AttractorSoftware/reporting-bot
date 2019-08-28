from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .settings import DevConfig
from .routes import blueprint

db = SQLAlchemy()
migrate = Migrate()


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(blueprint)

    from reporting_app import models

    db.init_app(app)
    migrate.init_app(app, db)
    return app
