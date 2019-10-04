from ..app import db
from ..models import Ticket


def get_all_tickets():
    return Ticket.query.all()


def create_ticket(code, title):
    t = Ticket(code=code, name=title)
    db.session.add(t)
    db.session.commit()
