import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


def html_color_to_json(html_color):
    if html_color.startswith("#"):
        html_color = html_color[1:]
    return {
        "red": int(html_color[0:2], 16) / 255.0,
        "green": int(html_color[2:4], 16) / 255.0,
        "blue": int(html_color[4:6], 16) / 255.0
    }


class SpreadsheetError(Exception):
    pass


class SpreadsheetNotSetError(SpreadsheetError):
    pass


class SheetNotSetError(SpreadsheetError):
    pass


class Spreadsheet:
    def __init__(self, json_key_file_name, debug_mode=False):
        self.debug_mode = debug_mode
        api_urls = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_file_name, api_urls)
        self.http_auth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.http_auth)
        self.drive_service = None  # Needed only for sharing
        self.spread_sheet_id = None
        self.sheet_id = None
        self.sheet_title = None
        self.requests = []
        self.value_ranges = []

    # Creates new spreadsheet
    def create(self, title, sheet_title="first", rows=1000, cols=26, locale='en_US', time_zone='Etc/GMT'):
        spreadsheet = self.service.spreadsheets().create(body={
            'properties': {'title': title, 'locale': locale, 'timeZone': time_zone},
            'sheets': [{'properties': {'sheetType': 'GRID', 'sheetId': 0, 'title': sheet_title,
                                       'gridProperties': {'rowCount': rows, 'columnCount': cols}}}]
        }).execute()
        if self.debug_mode:
            pprint(spreadsheet)
        self.spread_sheet_id = spreadsheet['spreadsheetId']
        self.sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']
        self.sheet_title = spreadsheet['sheets'][0]['properties']['title']

    def share(self, share_request_body):
        if self.spread_sheet_id is None:
            raise SpreadsheetNotSetError()
        if self.drive_service is None:
            self.drive_service = apiclient.discovery.build('drive', 'v3', http=self.http_auth)
        share_res = self.drive_service.permissions().create(
            fileId=self.spread_sheet_id,
            body=share_request_body,
            fields='id'
        ).execute()
        if self.debug_mode:
            pprint(share_res)

    def share_with_email_for_reading(self, email):
        self.share({'type': 'user', 'role': 'reader', 'emailAddress': email})

    def share_with_email_for_writing(self, email):
        self.share({'type': 'user', 'role': 'writer', 'emailAddress': email})

    def share_with_any_body_for_reading(self):
        self.share({'type': 'anyone', 'role': 'reader'})

    def share_with_anybody_for_writing(self):
        self.share({'type': 'anyone', 'role': 'writer'})

    def check_exists_file(self, spreadsheet_filename):
        if self.drive_service is None:
            self.drive_service = apiclient.discovery.build('drive', 'v3', http=self.http_auth)
        response = self.drive_service.files().list(q=f"name='{spreadsheet_filename}'").execute()
        files = response.get('files', [])
        return len(files) > 0

    def get_sheet_url(self):
        if self.spread_sheet_id is None:
            raise SpreadsheetNotSetError()
        if self.sheet_id is None:
            raise SheetNotSetError()
        return f'https://docs.google.com/spreadsheets/d/{self.spread_sheet_id}/edit#gid={str(self.sheet_id)}'

    # Sets current spreadsheet by id; set current sheet as first sheet of this spreadsheet
    def set_spread_sheet_by_id(self, spread_sheet_id):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=spread_sheet_id).execute()
        if self.debug_mode:
            pprint(spreadsheet)
        self.spread_sheet_id = spreadsheet['spreadsheetId']
        self.sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']
        self.sheet_title = spreadsheet['sheets'][0]['properties']['title']

    # spreadsheets.batchUpdate and spreadsheets.values.batchUpdate
    def run_prepared(self, value_input_option="USER_ENTERED"):
        if self.spread_sheet_id is None:
            raise SpreadsheetNotSetError()
        upd_first_res = {'replies': []}
        upd_second_res = {'responses': []}
        try:
            if len(self.requests) > 0:
                upd_first_res = self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spread_sheet_id,
                    body={"requests": self.requests}).execute()
                if self.debug_mode:
                    pprint(upd_first_res)
            if len(self.value_ranges) > 0:
                upd_second_res = self.service.spreadsheets().values().batchUpdate(
                    spreadsheetId=self.spread_sheet_id,
                    body={
                        "valueInputOption": value_input_option,
                        "data": self.value_ranges
                    }).execute()

                if self.debug_mode:
                    pprint(upd_second_res)
        finally:
            self.requests = []
            self.value_ranges = []
        return (upd_first_res['replies'], upd_second_res['responses'])

    def prepare_add_sheet(self, sheet_title, rows=1000, cols=26):
        self.requests.append({"addSheet": {"properties": {"title": sheet_title,
                                                          'gridProperties': {'rowCount': rows, 'columnCount': cols}}}})

    # Adds new sheet to current spreadsheet, sets as current sheet and returns it's id
    def add_sheet(self, sheet_title, rows=1000, cols=26):
        if self.spread_sheet_id is None:
            raise SpreadsheetNotSetError()
        self.prepare_add_sheet(sheet_title, rows, cols)
        added_sheet = self.run_prepared()[0][0]['addSheet']['properties']
        self.sheet_id = added_sheet['sheetId']
        self.sheet_title = added_sheet['title']
        return self.sheet_id

    def prepare_rename_sheet(self, new_title):
        self.requests.append({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": self.sheet_id,
                    "title": new_title,
                },
                "fields": "title"
            }
        })

    def rename_sheet(self, new_title):
        if self.spread_sheet_id is None:
            raise SpreadsheetNotSetError()
        self.prepare_rename_sheet(new_title)
        self.run_prepared()
        self.sheet_title = new_title
        return self.sheet_id

    def get_spreadsheet_sheets(self):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spread_sheet_id).execute()
        sheets = spreadsheet['sheets']
        return sheets

    def get_sheet_by_property(self, sheet_prop, comparison_value):
        sheets = self.get_spreadsheet_sheets()
        sheet = None
        for sh in sheets:
            if sh['properties'][sheet_prop] == comparison_value:
                sheet = sh['properties']
                break
        return sheet

    def set_sheet_by_title(self, sheet_title):
        sheet = self.get_sheet_by_property('title', sheet_title)
        self.sheet_id = sheet['sheetId']
        self.sheet_title = sheet['title']

    # Converts string range to GridRange of current sheet; examples:
    # "A3:B4"-> {sheetId: id of current sheet, startRowIndex: 2, endRowIndex: 4, startColumnIndex: 0, endColumnIndex: 2}
    # "A5:B" -> {sheetId: id of current sheet, startRowIndex: 4, startColumnIndex: 0, endColumnIndex: 2}
    def to_grid_range(self, cells_range):
        if self.sheet_id is None:
            raise SheetNotSetError()
        if isinstance(cells_range, str):
            start_cell, end_cell = cells_range.split(":")[0:2]
            cells_range = {}
            range_AZ = range(ord('A'), ord('Z') + 1)
            if ord(start_cell[0]) in range_AZ:
                cells_range["startColumnIndex"] = ord(start_cell[0]) - ord('A')
                start_cell = start_cell[1:]
            if ord(end_cell[0]) in range_AZ:
                cells_range["endColumnIndex"] = ord(end_cell[0]) - ord('A') + 1
                end_cell = end_cell[1:]
            if len(start_cell) > 0:
                cells_range["startRowIndex"] = int(start_cell) - 1
            if len(end_cell) > 0:
                cells_range["endRowIndex"] = int(end_cell)
        cells_range["sheetId"] = self.sheet_id
        return cells_range

    def prepare_set_dimension_pixel_size(self, dimension, start_index, end_index, pixel_size):
        if self.sheet_id is None:
            raise SheetNotSetError()
        self.requests.append({"updateDimensionProperties": {
            "range": {"sheetId": self.sheet_id,
                      "dimension": dimension,
                      "startIndex": start_index,
                      "endIndex": end_index},
            "properties": {"pixelSize": pixel_size},
            "fields": "pixelSize"}})

    def prepare_set_columns_width(self, start_col, end_col, width):
        self.prepare_set_dimension_pixel_size("COLUMNS", start_col, end_col + 1, width)

    def prepare_set_column_width(self, col, width):
        self.prepare_set_columns_width(col, col, width)

    def prepare_set_rows_height(self, startRow, endRow, height):
        self.prepare_set_dimension_pixel_size("ROWS", startRow, endRow + 1, height)

    def prepare_set_row_height(self, row, height):
        self.prepare_set_rows_height(row, row, height)

    def prepare_set_values(self, cells_range, values, major_dimension="ROWS"):
        if self.sheet_title is None:
            raise SheetNotSetError()
        self.value_ranges.append({"range": self.sheet_title + "!" + cells_range,
                                  "majorDimension": major_dimension, "values": values})

    def prepare_merge_cells(self, cells_range, merge_type="MERGE_ALL"):
        self.requests.append({"mergeCells": {"range": self.to_grid_range(cells_range), "mergeType": merge_type}})

    # format_json should be dict with userEnteredFormat to be applied to each cell
    def prepare_set_cells_format(self, cells_range, format_json, fields="userEnteredFormat"):
        self.requests.append({"repeatCell": {"range": self.to_grid_range(cells_range),
                                             "cell": {"userEnteredFormat": format_json}, "fields": fields}})

    # formats_json should be list of lists of dicts with userEnteredFormat for each cell in each row
    def prepare_set_cells_formats(self, cells_range, formats_json, fields="userEnteredFormat"):
        self.requests.append({"updateCells": {"range": self.to_grid_range(cells_range),
                                              "rows": [{"values": [{"userEnteredFormat": cell_format}
                                                                   for cell_format in row_formats]}
                                                       for row_formats in formats_json],
                                              "fields": fields}})

