from telebot import types
from ..app import db
from ..models import Project, Ticket

SELECT_PROJECT = 'select project'
NEW_REPORT = 'new report'
PROJECT_SUFFIX = 'project'
TICKET_SUFFIX = 'ticket'

user_dict = {}


def get_all_tickets():
    return Ticket.query.all()


def create_ticket(code, title):
    t = Ticket(code=code, name=title)
    db.session.add(t)
    db.session.commit()


def get_all_projects():
    return Project.query.all()


def create_projects_buttons():
    markup = types.InlineKeyboardMarkup()
    projects = get_all_projects()

    for project in projects:
        button = types.InlineKeyboardButton(project.name, callback_data=f'{project.name}-{PROJECT_SUFFIX}')
        markup.add(button)
    return markup


def show_tickets(m, bot):
    tickets_message = 'Please select ticket which assigned to you.'
    tickets_markup = create_tickets_buttons()
    bot.send_message(m.chat.id, tickets_message, reply_markup=tickets_markup)


def create_tickets_buttons():
    markup = types.InlineKeyboardMarkup()
    tickets = get_all_tickets()

    for ticket in tickets:
        button = types.InlineKeyboardButton(f'[{ticket.code}] - {ticket.name}', callback_data=f'{ticket.code}-{TICKET_SUFFIX}')
        markup.add(button)
    return markup
