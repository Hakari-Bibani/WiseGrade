Here's the fully updated code:
assignment2.py
Python
import streamlit as st
import os
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Step 1: Validate Student ID
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Enter Your Student ID")
    verify_button = st.button("Verify Student ID")

    if verify_button:
        try:
            # Load saved student IDs from Google Sheets for Assignment 1
            google_sheets_secrets = st.secrets.get("google_sheets", None)
            if not google_sheets_secrets:
                st.error("Google Sheets credentials are missing in Streamlit secrets.")
                return

            # Define the scope and authorize
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_secrets, scope)
            client = gspread.authorize(credentials)

            # Open the Google Sheet and get the student IDs
            spreadsheet = client.open_by_key(google_sheets_secrets["spreadsheet_id"])
            worksheet = spreadsheet.sheet1
            saved_ids = [row[2] for row in worksheet.get_all_values()[1:]]  # Assuming student_id is in the 3rd column

            if student_id in saved_ids:
                st.success(f"Student ID {student_id} verified. Proceed to the next steps.")
                st.session_state["verified"] = True
            else:
                st.error("Invalid Student ID. Please enter a valid ID from Assignment 1.")
                st.session_state["verified"] = False

        except Exception as e:
            st.error(f"An error occurred while verifying Student ID: {e}")
            st.session_state["verified"] = False

    # Proceed only if the student ID is verified
    if st.session_state.get("verified", False):
        # Step 2: Code Editor
        st.header("Step 2: Paste Your Code")
        code = st.text_area("Write your Python code here", height=300)

        # Step 3: Upload Files
        st.header("Step 3: Upload Your Outputs")
        uploaded_html = st.file_uploader("Upload your HTML file (Map)", type=["html"])
        uploaded_png = st.file_uploader("Upload your PNG file (Bar Chart)", type=["png"])
        uploaded_csv = st.file_uploader("Upload your CSV file (Summary)", type=["csv"])

        # Check if all files are uploaded
        all_uploaded = all([uploaded_html, uploaded_png, uploaded_csv])
        st.write("All files uploaded:", "✅ Yes" if all_uploaded else "❌ No")

        # Step 4: Submit Assignment
        if all_uploaded:
            submit_button = st.button("Submit Assignment")

            if submit_button:
                try:
                    # Save uploaded files temporarily
                    temp_dir = "temp_uploads"
                    os.makedirs(temp_dir, exist_ok=True)
                    html_path = os.path.join(temp_dir, "earthquake_map.html")
                    png_path = os.path.join(temp_dir, "earthquake_bar_chart.png")
                    csv_path = os.path.join(temp_dir, "earthquake_summary.csv")

                    with open(html_path, "wb") as f:
                        f.write(uploaded_html.getvalue())
                    with open(png_path, "wb") as f:
                        f.write(uploaded_png.getvalue())
                    with open(csv_path, "wb") as f:
                        f.write(uploaded_csv.getvalue())

                    # Grade the submission
                    grade = grade_assignment(code, html_path, png_path, csv_path)
                    st.success(f"Your grade for Assignment 2: {grade}/100")

                    # Update Google Sheets
                    update_google_sheet(
                        full_name="",  
                        email="",      
                        student_id=student_id,
                        grade=grade,
                        current_assignment="assignment_2"
                    )

                except Exception as e:
                    st.error(f"An error occurred during submission: {e}")

        else:
            st.warning("Please upload all required files to proceed.")

if __name__ == "__main__":
    show()
grade2.py
Python
import ast
import re
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import numpy as np

def grade_assignment(code, html_path, png_path, csv_path):
    total_points = 100
    grade = 0

    # 1. Library Imports (20 points)
    points = 20
    required_imports = ['requests', 'folium', 'pandas']
    try:
        tree = ast.parse(code)
        imports = [node.names[0].name for node in ast.walk(tree) if
