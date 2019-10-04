from flask_admin.contrib.sqla import ModelView


def init_admin_views(admin, db, models):
    admin.add_view(ModelView(models.User, db.session))
    admin.add_view(ModelView(models.Ticket, db.session))
    admin.add_view(ModelView(models.Project, db.session))
    admin.add_view(ModelView(models.Report, db.session))
    admin.add_view(ModelView(models.ProjectMember, db.session))
    admin.add_view(ModelView(models.Spreadsheet, db.session))
    admin.add_view(ModelView(models.SheetRole, db.session))
