import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and connect to Google Sheets API
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_credentials"], scope)
    client = gspread.authorize(creds)
    return client

# Fetch student record by student_id
def fetch_student_record(student_id):
    client = authenticate_google_sheets()
    sheet = client.open("WG").sheet1  # Replace with your sheet name
    records = sheet.get_all_records()
    for record in records:
        if record["student_ID"] == student_id:
            return record
    return None

# Update student record in Google Sheet
def update_student_record(student_id, assignment_number, score):
    client = authenticate_google_sheets()
    sheet = client.open("WG").sheet1  # Replace with your sheet name
    records = sheet.get_all_records()
    for i, record in enumerate(records):
        if record["student_ID"] == student_id:
            # Update the specific assignment or quiz score
            row_index = i + 2  # +2 because Google Sheets is 1-indexed and the first row is headers
            sheet.update_cell(row_index, assignment_number + 3, score)  # +3 to skip full_name, email, student_ID
            return True
    return False
