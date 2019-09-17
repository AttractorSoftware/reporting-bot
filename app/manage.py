from reporting_app.app import app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()
