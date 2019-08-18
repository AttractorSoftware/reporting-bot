from flask import Flask
from .settings import DevConfig
from .routes import blueprint


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(blueprint)
    return app
