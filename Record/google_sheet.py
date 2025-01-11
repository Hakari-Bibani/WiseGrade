import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def update_google_sheet(full_name, email, student_id, grade, current_assignment):
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

        # Check if email exists in the sheet
        try:
            cell = worksheet.find(email)  # Locate email in the sheet
        except gspread.exceptions.APIError:
            cell = None

        if cell:
            # If email exists, check if resubmission is allowed
            row = cell.row
            all_columns = worksheet.row_values(1)
            current_assignment_index = all_columns.index(current_assignment)

            # Check for later submissions
            for col in all_columns[current_assignment_index + 1:]:
                col_value = worksheet.cell(row, all_columns.index(col) + 1).value
                if col_value and col_value.strip():
                    st.error(f"Resubmission not allowed for {current_assignment} as later assignments are already submitted.")
                    return

            # Update the grade for the current assignment
            worksheet.update_cell(row, current_assignment_index + 1, grade)
            st.success(f"Resubmission successful for {current_assignment}. Your grade: {grade}/100")
        else:
            # Add a new row for the student if email doesn't exist
            all_columns = worksheet.row_values(1)
            new_row = [full_name, email, student_id] + [""] * (len(all_columns) - 3)
            new_row[all_columns.index(current_assignment)] = grade
            worksheet.append_row(new_row)
            st.success(f"Submission successful for {current_assignment}. Your grade: {grade}/100")

    except gspread.exceptions.APIError as e:
        st.error(f"Google Sheets API Error: {e}")
    except KeyError as e:
        st.error(f"Missing key in Streamlit secrets: {e}")
    except Exception as e:
        st.error(f"An error occurred while updating the Google Sheet: {e}")
