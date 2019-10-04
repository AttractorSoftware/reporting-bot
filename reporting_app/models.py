from .app import db
from datetime import datetime


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}>'


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text())
    project_id = db.Column(db.ForeignKey(Project.id))

    project = db.relationship('Project', foreign_keys='Ticket.project_id')

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


class ProjectMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))

    user = db.relationship('User', foreign_keys='ProjectMember.user_id')
    project = db.relationship('Project', foreign_keys='ProjectMember.project_id')

    def __repr__(self):
        return f'<id: {self.id}, user: {self.user.name} {self.user.last_name}, project: {self.project.name}>'


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.id))
    time_spent = db.Column(db.Integer)
    status = db.Column(db.String(30))
    created = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', foreign_keys='Report.user_id')
    ticket = db.relationship('Ticket', foreign_keys='Report.ticket_id')

    def __repr__(self):
        return f'<id: {self.id}, ticket name: {self.ticket.code}>'


class Spreadsheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    spreadsheet_id = db.Column(db.String(255), unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    project = db.relationship('Project', foreign_keys='Spreadsheet.project_id')

    def __repr__(self):
        return f'<id: {self.id}, filename: {self.filename}>'


class SheetRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    sheet_role_type = db.Column(db.String(25), default="writer")
    user = db.relationship('User', foreign_keys='SheetRole.user_id')
    project = db.relationship('Project', foreign_keys='SheetRole.project_id')

    def __repr__(self):
        return f'<id: {self.id}, filename: {self.filename}>'
