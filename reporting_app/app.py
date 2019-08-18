from flask import Flask
from .settings import DevConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    return app
