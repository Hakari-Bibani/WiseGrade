import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def update_google_sheet(full_name, email, student_id, grade, column_name):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Load credentials from Streamlit secrets
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["google_sheets"], scope
    )

    # Authorize the client
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
        # Add a new row
        new_row = [full_name, email, student_id] + [""] * (worksheet.col_count - 3)
        new_row[worksheet.find(column_name).col - 1] = grade
        worksheet.append_row(new_row)
