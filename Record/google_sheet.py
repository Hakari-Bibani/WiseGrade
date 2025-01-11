import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def update_google_sheet(full_name, email, student_id, grade, column_name):
    try:
        # Load secrets
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

        # Ensure the column exists
        col_cell = worksheet.find(column_name)
        if not col_cell:
            st.error(f"Column '{column_name}' not found in the sheet. Please check the column headers.")
            return

        # Check if email already exists in the sheet
        cell = worksheet.find(email)
        if cell:
            # If email exists, update the grade
            row = cell.row
            worksheet.update_cell(row, col_cell.col, grade)
            st.success(f"Updated grade for {email} in column '{column_name}'.")
        else:
            # If email doesn't exist, append a new row
            new_row = [full_name, email, student_id] + [""] * (worksheet.col_count - 3)
            new_row[col_cell.col - 1] = grade
            worksheet.append_row(new_row)
            st.success(f"Added new row for {email} with grade in column '{column_name}'.")

    except gspread.exceptions.CellNotFound:
        st.error(f"The column '{column_name}' or email '{email}' was not found.")
    except KeyError as e:
        st.error(f"Missing key in Streamlit secrets: {e}")
    except Exception as e:
        st.error(f"An error occurred while updating the Google Sheet: {e}")
