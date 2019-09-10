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
    project_id = db.Column(db.ForeignKey(Project.id))

    project = db.relationship('Project', foreign_keys='Task.project_id')

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


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id))
    time_spent = db.Column(db.Integer)
    status = db.Column(db.String(30))

    user = db.relationship('User', foreign_keys='Report.user_id')
    task = db.relationship('Task', foreign_keys='Report.task_id')

    def __repr__(self):
        return f'<id: {self.id}, ticket name: {self.task.code}>'
