from .app import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text())

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True)
    telegram_id = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name} {self.last_name}>'
