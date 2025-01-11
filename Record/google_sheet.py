# google_sheet.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Debug: Print all secrets
st.write("Secrets:", st.secrets)

# Authenticate and connect to Google Sheets API
def authenticate_google_sheets():
    try:
        # Use Streamlit secrets to get Google Sheets API credentials
        creds_dict = st.secrets["google_credentials"]
        st.write("Credentials found in secrets.toml.")
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client
    except KeyError:
        st.error("Google Sheets API credentials not found in secrets.toml. Please add them.")
        return None
    except Exception as e:
        st.error(f"Failed to authenticate with Google Sheets API: {e}")
        return None

# Save data to Google Sheet
def save_to_sheet(data):
    try:
        client = authenticate_google_sheets()
        if not client:
            st.error("Google Sheets authentication failed.")
            return False

        # Open the Google Sheet by name
        sheet = client.open("WG").sheet1  # Replace "WG" with your Google Sheet name

        # Append the data as a new row
        row = [
            data["full_name"],
            data["email"],
            data["student_ID"],
            data["assignment_1"],
        ]
        sheet.append_row(row)
        return True
    except gspread.exceptions.APIError as e:
        st.error(f"Google Sheets API error: {e}")
        return False
    except Exception as e:
        st.error(f"Failed to save data to Google Sheet: {e}")
        return False
