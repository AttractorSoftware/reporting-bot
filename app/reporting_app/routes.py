from flask import Blueprint, request, abort
from telebot import types
from .settings import DevConfig as config
from .app import bot

blueprint = Blueprint('reporting_app', __name__)


@blueprint.route('/')
def index():
    return 'Hello World'


@blueprint.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)
