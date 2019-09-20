import os


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    DATA_DIR = os.path.join(ROOT, 'data')
    API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
    WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

    WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
    WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(Config.DATA_DIR, 'app.sqlite3'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'development key'


class TestConfig(Config):
    ENV = 'test'
    TESTING = True
    DEBUG = True
    API_TOKEN = ''


configs = {
    'DEV': DevConfig,
    'TEST': TestConfig
}
