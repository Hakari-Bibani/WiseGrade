import streamlit as st
import traceback
import os
from grade2 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Verify Student ID
    st.header("Step 1: Verify Your Student ID")
    student_id = st.text_input("Enter Your Student ID", key="student_id")
    verify_button = st.button("Verify Student ID")

    student_verified = False
    if verify_button:
        try:
            # Load Google Sheets credentials
            google_sheets_secrets = st.secrets.get("google_sheets", None)
            if not google_sheets_secrets:
                st.error("Google Sheets credentials are missing in Streamlit secrets.")
                return

            # Connect to the Google Sheet
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials

            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_secrets, scope)
            client = gspread.authorize(credentials)
            spreadsheet = client.open_by_key(google_sheets_secrets["spreadsheet_id"])
            worksheet = spreadsheet.sheet1

            # Check if the Student ID exists
            student_row = worksheet.find(student_id).row
            student_verified = True
            st.success(f"Student ID {student_id} verified. You may proceed.")
        except gspread.exceptions.CellNotFound:
            st.error("Student ID not found. Please make sure you submitted Assignment 1.")
        except Exception as e:
            st.error(f"An error occurred during verification: {e}")

    if not student_verified:
        return  # Stop here if student is not verified

    # Section 2: Assignment Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Criteria"])

    with tab1:
        st.markdown("""
        ### Objective
        Analyze earthquake data using the USGS API, and visualize the results.
        
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

    # Analyze Button
    st.subheader("3. Analyze Your Submission")
    analyze_button = st.button("Analyze Submission")

    if analyze_button:
        if not code_input or not html_file or not bar_chart_file or not summary_file:
            st.error("Please provide all required files (HTML, PNG, CSV) and your code.")
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

                # Run the grading function
                grade = grade_assignment(code_input, html_path, bar_chart_path, summary_path)
                st.success(f"Your grade is: {grade}/100")

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
                st.text(traceback.format_exc())

    # Submission Button
    st.subheader("4. Submit Your Assignment")
    submit_button = st.button("Submit Assignment")

    if submit_button:
        if student_verified and code_input and html_file and bar_chart_file and summary_file:
            try:
                # Call the Google Sheets update function
                full_name = "Student Full Name"  # Replace with actual retrieval logic if needed
                email = "student_email@example.com"  # Replace with actual retrieval logic if needed
                update_google_sheet(full_name, email, student_id, grade, "assignment_2")
                st.success(f"Assignment 2 submitted successfully! Your grade: {grade}/100")
            except Exception as e:
                st.error(f"An error occurred during submission: {e}")
        else:
            st.error("Please verify your Student ID and ensure all files are uploaded before submission.")
