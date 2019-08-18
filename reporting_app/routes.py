from flask import Blueprint

blueprint = Blueprint('reporting_app', __name__)


@blueprint.route('/')
def index():
    return 'Hello World'
