import streamlit as st
import pandas as pd
from io import StringIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
from grades.grade2 import grade_assignment
import os

# Google Sheets API Setup
def get_google_sheet_data(sheet_id, range_name, creds_file="path_to_service_account.json"):
    """Fetch data from Google Sheets."""
    credentials = service_account.Credentials.from_service_account_file(creds_file, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    return result.get("values", [])

def save_to_google_sheet(sheet_id, range_name, values, creds_file="path_to_service_account.json"):
    """Save data to Google Sheets."""
    credentials = service_account.Credentials.from_service_account_file(creds_file, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    body = {"values": values}
    sheet.values().append(spreadsheetId=sheet_id, range=range_name, valueInputOption="USER_ENTERED", body=body).execute()

# Streamlit App
def show():
    # Google Sheets Configuration
    GOOGLE_SHEET_ID = "your_google_sheet_id"
    ASSIGNMENT_1_RANGE = "assignment_1!A:C"
    ASSIGNMENT_2_RANGE = "assignment_2!A:E"

    # Fetch valid Student IDs
    assignment_1_data = get_google_sheet_data(GOOGLE_SHEET_ID, ASSIGNMENT_1_RANGE)
    valid_student_ids = [row[2] for row in assignment_1_data]  # Assuming column C contains Student IDs

    st.title("Assignment 2: Earthquake Data Analysis")

    # Step 1: Validate Student ID
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Enter your Student ID")
    if student_id not in valid_student_ids:
        st.error("Invalid Student ID. Please enter a valid ID.")
        return  # Exit the app if the ID is invalid

    # Step 2: Code Cell
    st.header("Step 2: Paste Your Code")
    code = st.text_area("Paste your Python code here", height=300)

    # Step 3: File Uploads
    st.header("Step 3: Upload Your Outputs")
    uploaded_html = st.file_uploader("Upload your HTML Map File", type="html")
    uploaded_png = st.file_uploader("Upload your PNG Bar Chart", type="png")
    uploaded_csv = st.file_uploader("Upload your CSV Summary", type="csv")

    # Check if all files are uploaded
    if st.button("Check Files"):
        if not all([uploaded_html, uploaded_png, uploaded_csv]):
            st.error("Please upload all required files before proceeding.")
        else:
            st.success("All required files uploaded successfully.")

    # Step 4: Submit and Grade
    if st.button("Submit Assignment"):
        if not all([uploaded_html, uploaded_png, uploaded_csv]):
            st.error("Please upload all required files before submission.")
            return

        # Save uploaded files temporarily
        uploaded_html_path = os.path.join("grades", "uploaded_map.html")
        uploaded_png_path = os.path.join("grades", "uploaded_chart.png")
        uploaded_csv_path = os.path.join("grades", "uploaded_summary.csv")

        with open(uploaded_html_path, "wb") as f:
            f.write(uploaded_html.read())
        with open(uploaded_png_path, "wb") as f:
            f.write(uploaded_png.read())
        with open(uploaded_csv_path, "wb") as f:
            f.write(uploaded_csv.read())

        # Grade the assignment
        grade = grade_assignment(code, uploaded_html_path, uploaded_png_path, uploaded_csv_path)

        # Display grade and save to Google Sheets
        st.success(f"Your grade: {grade}/100")
        save_to_google_sheet(
            GOOGLE_SHEET_ID,
            ASSIGNMENT_2_RANGE,
            [[student_id, grade]],
        )
        st.info("Your grade has been recorded in Google Sheets.")

if __name__ == "__main__":
    show()
