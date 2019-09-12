from reporting_app.app import create_app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from reporting_app.settings import DevConfig

app = create_app(DevConfig)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host=app.config['WEBHOOK_LISTEN']))


if __name__ == '__main__':
    manager.run()
