import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and connect to Google Sheets API
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_credentials"], scope)
    client = gspread.authorize(creds)
    return client

# Save data to Google Sheet
def save_to_sheet(data):
    client = authenticate_google_sheets()
    sheet = client.open("WG").sheet1  # Replace with your sheet name
    sheet.append_row([data["full_name"], data["email"], data["student_ID"], data["assignment_1"]])
