import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_google_sheet(full_name, email, student_id, grade, column_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    spreadsheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])
    worksheet = spreadsheet.sheet1

    # Find or update the row based on email
    cell = worksheet.find(email)
    if cell:
        row = cell.row
        worksheet.update_cell(row, column_name, grade)
    else:
        new_row = [full_name, email, student_id] + [""] * (worksheet.col_count - 3)
        new_row[worksheet.find(column_name).col - 1] = grade
        worksheet.append_row(new_row)
