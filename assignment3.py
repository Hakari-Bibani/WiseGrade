import streamlit as st
import os
import pandas as pd

# Import from subdirectories (make sure your repo has __init__.py in these folders)
from grades.grade3 import grade_assignment  # Ensure this path is correct in your project
from Record.google_sheet import update_google_sheet  # Ensure this path is correct in your project

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
            In this assignment, you will extend your earthquake data analysis from Assignment 2.
            You will fetch real-time earthquake data, perform advanced filtering, and create interactive visualizations.
            Additionally, you will analyze trends and generate a report.
            """)
            # Add "See More" expandable section
            with st.expander("See More"):
                st.markdown("""
            ### Task Requirements
            - **Fetch Earthquake Data**:
                - Use the USGS Earthquake API to fetch data for the date range **January 10th, 2025, to January 17th, 2025**.
                - The API URL is:  
                  `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=YYYY-MM-DD&endtime=YYYY-MM-DD`.  
                  Replace `YYYY-MM-DD` with the appropriate dates.
            - **Advanced Filtering**:
                - Filter the data to include only earthquakes with a magnitude greater than 4.5.
            - **Interactive Map**:
                - Create an interactive map using `folium` to show the locations of the filtered earthquakes.
                - Use custom icons for markers based on magnitude ranges.
            - **Trend Analysis**:
                - Generate a line chart showing the frequency of earthquakes over time.
            - **Report Generation**:
                - Create a PDF report summarizing your findings.
            ### Python Libraries You Will Use
            - `folium` for the map.
            - `matplotlib` or `seaborn` for the line chart.
            - `requests` or `urllib` for API calls.
            - `pandas` for data processing.
            - `reportlab` for PDF generation.
            ### Expected Output
            1. An interactive map showing earthquake locations.
            2. A line chart showing earthquake frequency over time.
            3. A PDF report summarizing your analysis.
            """)

        with tab2:
            st.markdown("""
            ### Detailed Grading Breakdown
            #### 1. Library Imports (10 Points)
            - Checks if the required libraries (`folium`, `matplotlib`, `requests`, `pandas`, `reportlab`) are imported.
            """)
            # Add "See More" expandable section
            with st.expander("See More"):
                st.markdown("""
            #### 2. Code Quality (20 Points)
            - **Variable Naming (5 Points)**:
                - Deducted if non-descriptive variable names are used (e.g., `x`, `y`).
            - **Spacing (5 Points)**:
                - Deducted if improper spacing is found (e.g., no space after `=`, `>`, `<`).
            - **Comments (5 Points)**:
                - Deducted if no comments are present to explain major steps.
            - **Code Organization (5 Points)**:
                - Deducted if code blocks are not logically separated with blank lines.
            #### 3. Fetching Data from the API (10 Points)
            - **Correct API URL (5 Points)**:
                - Deducted if the URL is incorrect or the date range is invalid.
            - **Successful Data Retrieval (5 Points)**:
                - Deducted if the data is not fetched successfully or error handling is missing.
            #### 4. Advanced Filtering (10 Points)
            - **Correct Filtering (5 Points)**:
                - Deducted if earthquakes with magnitude ≤ 4.5 are included.
            - **Data Extraction (5 Points)**:
                - Deducted if relevant data (latitude, longitude, magnitude, time) is not extracted.
            #### 5. Interactive Map (20 Points)
            - **Map Generation (5 Points)**:
                - Deducted if the map is not generated or displayed.
            - **Custom Icons (10 Points)**:
                - Deducted if custom icons are not used based on magnitude ranges.
            - **Popups (5 Points)**:
                - Deducted if popups do not display:
                    - Magnitude: 2 points
                    - Latitude and Longitude: 2 points
                    - Time in readable format: 1 point
            #### 6. Trend Analysis (20 Points)
            - **Line Chart Generation (10 Points)**:
                - Deducted if the line chart is not generated or displayed.
            - **Labeling (10 Points)**:
                - Deducted if the chart is not properly labeled (title, x-axis, y-axis).
            #### 7. Report Generation (20 Points)
            - **PDF Report (10 Points)**:
                - Deducted if the PDF report is not generated.
            - **Content Quality (10 Points)**:
                - Deducted if the report does not summarize findings clearly.
            """)

        # Step 3: Code Submission and Output
        st.header("Step 3: Run and Submit Your Code")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Step 4: Upload HTML File
        st.header("Step 4: Upload Your HTML File (Interactive Map)")
        uploaded_html = st.file_uploader("Upload your HTML file (Map)", type=["html"])

        # Step 5: Upload Google Sheet as Excel File
        st.header("Step 5: Upload Your Google Sheet (Excel File)")
        uploaded_excel = st.file_uploader("Upload your Google Sheet as an Excel file", type=["xlsx"])

        # Step 6: Submit Assignment
        st.header("Step 6: Submit Assignment")
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate that all required files are uploaded
                if uploaded_html is None:
                    st.error("Please upload an HTML file for the interactive map.")
                    return
                if uploaded_excel is None:
                    st.error("Please upload your Google Sheet as an Excel file.")
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

                # Update Google Sheets with the numerical grade under "assignment_3"
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
