from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from .settings import DevConfig
from .routes import blueprint
from .admin import init_admin_views


db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name="reporting", template_mode="bootstrap3")


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(blueprint)

    from reporting_app import models

    db.init_app(app)
    migrate.init_app(app, db)

    admin.init_app(app)
    init_admin_views(admin, db, models)
    return app
