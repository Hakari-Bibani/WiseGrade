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

        # Fetch headers from the sheet
        headers = worksheet.row_values(1)  # First row contains column headers
        if column_name not in headers:
            st.error(f"Column '{column_name}' not found in the sheet. Available columns: {headers}")
            return

        # Get the column index
        col_index = headers.index(column_name) + 1

        # Check if email already exists in the sheet
        cell = worksheet.find(email)
        if cell:
            # If email exists, update the grade
            row = cell.row
            worksheet.update_cell(row, col_index, grade)
            st.success(f"Updated grade for {email} in column '{column_name}'.")
        else:
            # If email doesn't exist, append a new row
            new_row = [full_name, email, student_id] + [""] * (len(headers) - 3)
            new_row[col_index - 1] = grade
            worksheet.append_row(new_row)
            st.success(f"Added new row for {email} with grade in column '{column_name}'.")

    except gspread.exceptions.APIError as e:
        st.error(f"An API error occurred while interacting with Google Sheets: {e}")
    except KeyError as e:
        st.error(f"Missing key in Streamlit secrets: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred while updating the Google Sheet: {e}")
