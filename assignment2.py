import streamlit as st
import os
import traceback
from grade2 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Verify Student ID
    st.header("Step 1: Verify Your Student ID")
    student_id = st.text_input("Enter Your Student ID", key="student_id")
    
    # Check if the student ID is valid (exists in Google Sheet for Assignment 1)
    student_verified = False
    if st.button("Verify Student ID"):
        try:
            # Connect to Google Sheets
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials

            google_sheets_secrets = st.secrets.get("google_sheets", None)
            if not google_sheets_secrets:
                st.error("Google Sheets credentials are missing in Streamlit secrets.")
                return

            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_secrets, scope)
            client = gspread.authorize(credentials)
            spreadsheet = client.open_by_key(google_sheets_secrets["spreadsheet_id"])
            worksheet = spreadsheet.sheet1

            # Check if the student ID exists
            cell = worksheet.find(student_id)
            student_verified = True
            st.success(f"Student ID {student_id} verified. You may proceed.")
        except gspread.exceptions.CellNotFound:
            st.error("Student ID not found. Please make sure you submitted Assignment 1.")
        except Exception as e:
            st.error(f"An error occurred during verification: {e}")

    if not student_verified:
        return  # Stop further execution if student is not verified

    # Section 2: Assignment Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Criteria"])

    with tab1:
        st.markdown("""
        ### Objective
        Analyze earthquake data using the USGS API and visualize the results.
        
        **Key Tasks**:
        - Fetch earthquake data (Jan 2 - Jan 9, 2025).
        - Filter earthquakes with magnitude > 4.0.
        - Create a map with color-coded markers for magnitude ranges.
        - Create a bar chart showing earthquake counts by magnitude ranges.
        - Provide a text summary with detailed statistics.
        """)

    with tab2:
        st.markdown("""
        ### Grading Criteria
        - **Library Imports (10%)**
        - **Code Quality (20%)**
        - **Data Retrieval (10%)**
        - **Data Filtering (10%)**
        - **Map Visualization (20%)**
        - **Bar Chart Comparison (15%)**
        - **Text Summary Accuracy (15%)**
        """)

    # Section 3: Submission
    st.header("Step 3: Submit Your Code and Outputs")

    # Code Cell
    st.subheader("1. Paste Your Code")
    code_input = st.text_area("Paste your Python code here", height=300)

    # File Uploads
    st.subheader("2. Upload Your Outputs")
    html_file = st.file_uploader("Upload HTML Map File", type=["html"])
    bar_chart_file = st.file_uploader("Upload PNG Bar Chart", type=["png"])
    summary_file = st.file_uploader("Upload CSV Summary", type=["csv"])

    # Check Button
    st.subheader("3. Check Submission")
    if st.button("Check"):
        if not code_input:
            st.error("Code cell is empty. Please paste your Python code.")
        if not html_file:
            st.error("HTML file is missing. Please upload the HTML file.")
        if not bar_chart_file:
            st.error("Bar chart PNG is missing. Please upload the PNG file.")
        if not summary_file:
            st.error("CSV summary file is missing. Please upload the CSV file.")
        if code_input and html_file and bar_chart_file and summary_file:
            st.success("All required files and code are provided. You may proceed to submit.")

    # Submit Button
    st.subheader("4. Submit Your Assignment")
    if st.button("Submit"):
        if not code_input or not html_file or not bar_chart_file or not summary_file:
            st.error("Please ensure all required files and code are provided before submission.")
        else:
            try:
                # Save uploaded files temporarily
                html_path = os.path.join("temp", "map.html")
                bar_chart_path = os.path.join("temp", "bar_chart.png")
                summary_path = os.path.join("temp", "summary.csv")

                with open(html_path, "wb") as f:
                    f.write(html_file.read())
                with open(bar_chart_path, "wb") as f:
                    f.write(bar_chart_file.read())
                with open(summary_path, "wb") as f:
                    f.write(summary_file.read())

                # Grade the assignment
                grade = grade_assignment(code_input, html_path, bar_chart_path, summary_path)
                st.success(f"Your grade is: {grade}/100")

                # Save the grade to Google Sheets
                full_name = "Student Full Name"  # Replace with actual retrieval logic
                email = "student_email@example.com"  # Replace with actual retrieval logic
                update_google_sheet(full_name, email, student_id, grade, "assignment_2")

                st.success(f"Assignment 2 submitted successfully! Your grade: {grade}/100")
            except Exception as e:
                st.error(f"An error occurred during submission: {e}")
                st.text(traceback.format_exc())
