from datetime import datetime
from sqlalchemy import and_
from .google_spread_sheet import Spreadsheet
from .models import Report, Project, Ticket, User, ProjectMember, Spreadsheet as SpreadsheetModel


class ReportRepo(object):
    def get_user_reports_by_project(self, user_id, project_id):
        reports_records = Report.query.join(Ticket).join(Project).join(User).filter(
            and_(User.id == user_id, Project.id == project_id)
        ).all()
        reports = list(map(lambda report: {
            'user': f'{report.user.name} {report.user.last_name}',
            'code': report.ticket.code,
            'title': report.ticket.name,
            'comment': report.comment,
            'time_spent': report.time_spent,
            'date': report.created.strftime('%d.%m.%Y')
        }, reports_records))
        return reports

    def get_project_spread_sheet(self, project_id, spreadsheet_name):
        spreadsheet = SpreadsheetModel.query.join(Project).filter(
            and_(Project.id == project_id, SpreadsheetModel.filename == spreadsheet_name)).first()
        spreadsheet_query = {
            'filename': spreadsheet.filename,
            'spreadsheet_id': spreadsheet.spreadsheet_id
        }
        return spreadsheet_query

    def get_projects_members(self, project_id):
        members = ProjectMember.query.join(Project).filter(Project.id == project_id).all()
        users = list(map(lambda member: {
            "name": member.user.name,
            "last_name": member.user.last_name,
            "phone": member.user.phone,
            "email": member.user.email
        }, members))
        return users


class SendProjectGoogleSpreadSheetUseCase(object):
    def __init__(self, repo, credentials):
        self.repo = repo
        self.credentials = credentials

    def execute(self, project_id, user_id):
        reports = self.repo.get_user_reports_by_project(user_id, project_id)
        members = self.repo.get_projects_members(project_id)
        if not reports:
            return
        queries = []
        for report in reports:
            query = [
                report['date'],
                report['user'],
                report['comment'],
                round(report['time_spent']/60, 2),  # to hours
                report['code']
            ]
            queries.append(query)
        emails = list(map(lambda member: member['email'], members))
        self.write(queries, emails, project_id, user_id)

    def get_name_of_timesheet(self, project: str) -> str:
        current_date = datetime.now()
        month = current_date.strftime("%B")
        year = current_date.strftime("%Y")
        file_name = f'{month} {project} {year} Timesheet'
        return file_name

    def write(self, reports, emails, project_id, user_id):
        sheet = Spreadsheet(self.credentials)
        spreadsheet_name = self.get_name_of_timesheet(project_id)
        if sheet.check_exists_file(spreadsheet_name):
            spreadsheet = self.repo.get_project_spread_sheet(project_id, spreadsheet_name)
            sheet_id = spreadsheet['spreadsheet_id']
            sheet.set_spread_sheet_by_id(sheet_id)
        else:
            sheet.create(spreadsheet_name, time_zone="Asia/Bishkek")
        sheet.prepare_set_values("A1:E1", [['Date', 'Name', 'Task', 'Hours', 'Code']])
        sheet.prepare_set_cells_format("A1:E1", {"textFormat": {"bold": True}})
        sheet.prepare_set_values(f'A2:E{len(reports) + 2}', reports)
        sheet.run_prepared()
        for email in emails:
            sheet.share_with_email_for_writing(email)
        return sheet.spread_sheet_id
