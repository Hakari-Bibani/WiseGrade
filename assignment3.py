import streamlit as st
import os
import pandas as pd
from grades.grade3 import grade_assignment  # Ensure this path is correct in your project
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 3: Advanced Earthquake Data Analysis")

    # Prevent re-submission: if the user has already submitted assignment 3, disable resubmission.
    if st.session_state.get("assignment3_submitted", False):
        st.warning("You have already submitted Assignment 3. Resubmission is not allowed.")
        return

    # Step 1: Validate Student ID
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Enter Your Student ID")
    verify_button = st.button("Verify Student ID")

    if verify_button:
        try:
            google_sheets_secrets = st.secrets.get("google_sheets", None)
            if not google_sheets_secrets:
                st.error("Google Sheets credentials are missing in Streamlit secrets.")
                return

            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_secrets, scope)
            client = gspread.authorize(credentials)

            spreadsheet = client.open_by_key(google_sheets_secrets["spreadsheet_id"])
            worksheet = spreadsheet.sheet1
            saved_ids = [row[2].strip() for row in worksheet.get_all_values()[1:] if len(row) > 2]  # Assuming Student ID in 3rd column

            if student_id.strip() in saved_ids:
                st.success(f"Student ID {student_id} verified. Proceed to the next steps.")
                st.session_state["verified"] = True
            else:
                st.error("Invalid Student ID. Please enter a valid ID from Assignment 2.")
                st.session_state["verified"] = False

        except Exception as e:
            st.error(f"An error occurred while verifying Student ID: {e}")
            st.session_state["verified"] = False

    if st.session_state.get("verified", False):
        # Step 2: Assignment and Grading Details
        st.header("Step 2: Review Assignment Details")
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("""
            ### Objective
            In this assignment, you will extend your earthquake data analysis from Assignment 2. You will fetch real-time earthquake data, perform advanced filtering, and create interactive visualizations. Additionally, you will analyze trends and generate a report.
            """)

            with st.expander("See More"):
                st.markdown("""
            ### Task Requirements
            - Fetch real-time earthquake data.
            - Perform filtering and analysis.
            - Create an interactive map.
            - Generate a PDF report.
            - Filter data to separate rows below 25°C and above 25°C.
            """)

        with tab2:
            st.markdown("""
            ### Grading Breakdown
            #### Code Grading (40 Points)
            - Library Imports (20 Points)
            - JSON Path (10 Points)
            - Sheet Creation (10 Points)
            #### Uploaded HTML File (15 Points)
            - Markers with "blue" (5 Points)
            - Markers with "red" (10 Points)
            #### Uploaded Excel File (45 Points)
            - Compare sheet names, column names, and data equivalence.
            """)

        # Step 3: Code Submission and Output
        st.header("Step 3: Submit Your Assignment")
        code_input = st.text_area("Paste Your Code Here", height=300)

        # Step 4: Upload HTML File
        st.header("Step 4: Upload Your HTML File")
        uploaded_html = st.file_uploader("Upload your HTML file (Map)", type=["html"])

        # Step 5: Upload Excel File
        st.header("Step 5: Upload Your Excel File")
        uploaded_excel = st.file_uploader("Upload your Excel file", type=["xlsx"])

        # Submit Assignment
        st.header("Step 6: Submit Assignment")
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate uploads
                if uploaded_html is None:
                    st.error("Please upload an HTML file.")
                    return
                if uploaded_excel is None:
                    st.error("Please upload your Excel file.")
                    return

                # Save the uploaded files temporarily
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                # Save HTML file
                html_path = os.path.join(temp_dir, "uploaded_map.html")
                with open(html_path, "wb") as f:
                    f.write(uploaded_html.getvalue())

                # Save Excel file
                excel_path = os.path.join(temp_dir, "uploaded_sheet.xlsx")
                with open(excel_path, "wb") as f:
                    f.write(uploaded_excel.getvalue())

                # Path to the correct Excel file
                correct_excel_path = "grades/correct_assignment3.xlsx"

                # Grade the assignment
                grade = grade_assignment(code_input, html_path, excel_path, correct_excel_path)
                st.success(f"Your grade for Assignment 3: {grade}/100")

                # Update Google Sheets with the numerical grade
                update_google_sheet(
                    full_name="",  # Update if needed
                    email="",      # Update if needed
                    student_id=student_id,
                    grade=grade,
                    current_assignment="assignment_3"
                )

                # Prevent resubmission
                st.session_state["assignment3_submitted"] = True

                # Cleanup temporary files
                if os.path.exists(temp_dir):
                    import shutil
                    shutil.rmtree(temp_dir)

            except Exception as e:
                st.error(f"An error occurred during submission: {e}")

if __name__ == "__main__":
    show()
