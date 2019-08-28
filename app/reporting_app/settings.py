import os


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    DATA_DIR = os.path.join(ROOT, 'data')


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(Config.DATA_DIR, 'app.sqlite3'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    ENV = 'test'
    TESTING = True
    DEBUG = True
