import streamlit as st
import os
import pandas as pd
from grades.grade3 import grade_assignment  # Ensure this path is correct in your project
from Record.google_sheet import update_google_sheet

def check_assignment2_submission(student_id):
    """
    Checks if the student has already submitted Assignment 2.
    Returns True if they have, False otherwise.
    """
    try:
        google_sheets_secrets = st.secrets.get("google_sheets", None)
        if not google_sheets_secrets:
            st.error("Google Sheets credentials are missing in Streamlit secrets.")
            return False

        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_secrets, scope)
        client = gspread.authorize(credentials)

        spreadsheet = client.open_by_key(google_sheets_secrets["spreadsheet_id"])
        worksheet = spreadsheet.sheet1
        records = worksheet.get_all_records()

        for record in records:
            if record["Student ID"] == student_id and record["Assignment"] == "assignment_2":
                return True
        return False
    except Exception as e:
        st.error(f"Error checking Assignment 2 submission: {e}")
        return False

def show():
    st.title("Assignment 3: Advanced Earthquake Data Analysis")

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
            saved_ids = [row[2] for row in worksheet.get_all_values()[1:]]  # Assuming Student ID in 3rd column

            if student_id in saved_ids:
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
            # Add "See More" expandable section
            with st.expander("See More"):
                st.markdown("""
            ### Task Requirements
            - **Fetch Earthquake Data**:
                - Use the USGS Earthquake API to fetch data for the date range **January 10th, 2025, to January 17th, 2025**.
                - The API URL is:  
                  https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=YYYY-MM-DD&endtime=YYYY-MM-DD.  
                  Replace YYYY-MM-DD with the appropriate dates.
            - **Advanced Filtering**:
                - Filter the data to include only earthquakes with a magnitude greater than 4.5.
            - **Interactive Map**:
                - Create an interactive map using folium to show the locations of the filtered earthquakes.
                - Use custom icons for markers based on magnitude ranges.
            - **Trend Analysis**:
                - Generate a line chart showing the frequency of earthquakes over time.
            - **Report Generation**:
                - Create a PDF report summarizing your findings.
            ### Python Libraries You Will Use
            - folium for the map.
            - matplotlib or seaborn for the line chart.
            - requests or urllib for API calls.
            - pandas for data processing.
            - reportlab for PDF generation.
            ### Expected Output
            1. An interactive map showing earthquake locations.
            2. A line chart showing earthquake frequency over time.
            3. A PDF report summarizing your analysis.
            """)

        with tab2:
            st.markdown("""
            ### Detailed Grading Breakdown
            #### 1. Library Imports (10 Points)
            - Checks if the required libraries (folium, matplotlib, requests, pandas, reportlab) are imported.
            """)
            # Add "See More" expandable section
            with st.expander("See More"):
                st.markdown("""
            #### 2. Code Quality (10 Points)
            - **Variable Naming (5 Points)**:
                - Deducted if non-descriptive variable names are used (e.g., x, y).
            - **Spacing (5 Points)**:
                - Deducted if improper spacing is found (e.g., no space after =, >, <).
            - **Comments (5 Points)**:
                - Deducted if no comments are present to explain major steps.
            - **Code Organization (5 Points)**:
                - Deducted if code blocks are not logically separated with blank lines.
            #### 3. Using JSON API (10 Points)
            - **Correct API URL (5 Points)**:
                - Deducted if the URL is incorrect or the date range is invalid.
            - **Successful Data Retrieval (5 Points)**:
                - Deducted if the data is not fetched successfully or error handling is missing.
            #### 4. Encapsulate Functionality (5 Points)
            - **Encapsulation (5 Points)**:
                - Deducted if the functionality of the three scripts (Stage 1, Stage 2, and Stage 3) is not encapsulated into distinct functions.
            #### 5. Filter Data Below 25°C (5 Points)
            - **Correct Filtering (5 Points)**:
                - Deducted if the data is not filtered correctly for temperatures below 25°C.
            #### 6. Filter Data Above 25°C (5 Points)
            - **Correct Filtering (5 Points)**:
                - Deducted if the data is not filtered correctly for temperatures above 25°C.
            #### 7. HTML File (15 Points)
            - **Markers (5 Points)**:
                - Deducted if the HTML file does not contain markers (e.g., marker or circle-marker).
            - **Colors (10 Points)**:
                - Deducted if the HTML file does not contain the colors green (5 points) and red (5 points).
            #### 8. Excel File (25 Points)
            - **Sheet Names (15 Points)**:
                - Deducted if the Excel file does not contain sheets named Sheet1, Below_25, and Above_25 (5 points each).
            - **Column Names (5 Points)**:
                - Deducted if the sheets do not contain the columns longitude, latitude, and temperature (or equivalent).
            - **Row Counts (5 Points)**:
                - Deducted if the Below_25 sheet does not contain 264 rows (±3) or the Above_25 sheet does not contain 237 rows (±3).
            """)

        # Step 3: Code Submission and Output
        st.header("Step 3: Run and Submit Your Code")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Step 4: Upload HTML File
        st.header("Step 4: Upload Your HTML File (Interactive Map)")
        uploaded_html = st.file_uploader("Upload your HTML file (Map)", type=["html"])

        # Step 5: Upload Excel File
        st.header("Step 5: Upload Your Excel File (Google Sheet)")
        uploaded_excel = st.file_uploader("Upload your Excel file (Google Sheet)", type=["xlsx"])

        # Step 6: Submit Assignment
        st.header("Step 6: Submit Assignment")
        submit_button = st.button("Submit Assignment")

        if submit_button:
            if check_assignment2_submission(student_id):
                st.error("You have already submitted Assignment 2. You cannot resubmit it.")
            else:
                try:
                    # Validate that all required files are uploaded
                    if uploaded_html is None:
                        st.error("Please upload an HTML file for the interactive map.")
                        return
                    if uploaded_excel is None:
                        st.error("Please upload your Excel file (Google Sheet).")
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

                    # Grade the assignment
                    grade = grade_assignment(code_input, html_path, excel_path)
                    st.success(f"Your grade for Assignment 3: {grade}/100")

                    # Update Google Sheets with the numerical grade
                    update_google_sheet(
                        full_name="",  # Update if needed
                        email="",      # Update if needed
                        student_id=student_id,
                        grade=grade,
                        current_assignment="assignment_3"
                    )

                except Exception as e:
                    st.error(f"An error occurred during submission: {e}")

if __name__ == "__main__":
    show() 
