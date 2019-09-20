import telebot, time, logging, os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from .settings import configs
from .admin import init_admin_views


def run_in_webhook_mode(bot, config):
    bot.remove_webhook()
    time.sleep(0.1)
    bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH)


def run_in_polling_mode(bot):
    bot.polling()


migrate = Migrate()
admin = Admin(name="reporting", template_mode="bootstrap3")

config = configs[os.getenv('ENV', 'DEV')]
bot = telebot.TeleBot(config.API_TOKEN)
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
db.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)

from .routes import blueprint
app.register_blueprint(blueprint)
from reporting_app import models
init_admin_views(admin, db, models)

if os.getenv('ENV') != 'TEST':
    if config.WEBHOOK_HOST:
        run_in_webhook_mode(bot, config)
    else:
        run_in_polling_mode(bot)

logger = telebot.logger
logger.setLevel(logging.INFO)

from .bot import handlers
