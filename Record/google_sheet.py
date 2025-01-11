import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def update_google_sheet(full_name, email, student_id, grade, column_name):
    try:
        # Ensure the secrets are loaded
        google_sheets_secrets = st.secrets["google_sheets"]

        # Define the scope
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        # Load credentials from secrets
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_secrets, scope)

        # Authorize the client
        client = gspread.authorize(credentials)

        # Open the Google Sheet
        spreadsheet = client.open_by_key(google_sheets_secrets["spreadsheet_id"])
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

    except KeyError as e:
        st.error(f"Missing key in Streamlit secrets: {e}")
    except Exception as e:
        st.error(f"An error occurred while updating the Google Sheet: {e}")
