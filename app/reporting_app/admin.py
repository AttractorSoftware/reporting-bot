from flask_admin.contrib.sqla import ModelView


def init_admin_views(admin, db, models):
    admin.add_view(ModelView(models.User, db.session))
    admin.add_view(ModelView(models.Task, db.session))
    admin.add_view(ModelView(models.Project, db.session))
