import telebot, time, logging, os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from .settings import DevConfig as config

from .admin import init_admin_views

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])
migrate = Migrate()
admin = Admin(name="reporting", template_mode="bootstrap3")

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

bot.remove_webhook()
time.sleep(0.1)
bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH)

logger = telebot.logger
logger.setLevel(logging.INFO)

from .bot import handlers
