import streamlit as st
import os
from grades.grade3 import grade_assignment  # ensure this path is correct in your project
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 3: Geographical Temperature Data Analysis")

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
                st.error("Invalid Student ID. Please enter a valid ID from Assignment 1.")
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
            In this assignment, students will work with geographical temperature data and apply Python programming to perform data manipulation and visualization. The task is broken into three stages, with each stage encapsulating a specific function. By the end of the assignment, students will merge the functions into one script to complete the task efficiently.
            """)
            # Add "See More" expandable section
            with st.expander("See More"):
                st.markdown("""
            ### Stage 1: Filtering Data Below 25°C
            **Goal**: Create a new tab in the spreadsheet containing only the data points where the temperature is below 25°C.
            **Instructions**:
            - Load the provided Excel file containing longitude, latitude, and temperature data.
            - Write a Python script that filters out all the rows where the temperature is below 25°C.
            - Save this filtered data in a new sheet within the same Excel file, naming the new sheet "Below_25".
            **Deliverable**: A script that filters and saves the data in the "Below_25" tab of the Excel file.

            ### Stage 2: Filtering Data Above 25°C
            **Goal**: Create another tab in the spreadsheet containing only the data points where the temperature is above 25°C.
            **Instructions**:
            - Extend your script to filter out all the rows where the temperature is above 25°C.
            - Save this filtered data in a new sheet named "Above_25".
            **Deliverable**: A script that adds the "Above_25" tab to the Excel file.

            ### Stage 3: Visualizing Data on a Map
            **Goal**: Visualize the data points from both the "Below_25" and "Above_25" tabs on a geographical map.
            **Instructions**:
            - Using a Python mapping library (such as folium, matplotlib, or plotly), plot the data points from both the "Below_25" and "Above_25" tabs.
            - Use blue to represent the data points from the "Below_25" tab and red for the "Above_25" tab.
            - Ensure the map accurately displays the temperature data at the correct coordinates.
            **Deliverable**: A Python script that generates a map displaying the data points in blue and red.

            ### Final Task: Merging the Scripts
            **Goal**: Combine all three stages into one cohesive Python script that performs the filtering and visualization tasks in sequence.
            **Instructions**:
            - Encapsulate the functionality of the three scripts (Stage 1, Stage 2, and Stage 3) into distinct functions.
            - Write a master function that calls these functions in sequence:
                1. First, filter the data below 25°C and save it to a new tab.
                2. Then, filter the data above 25°C and save it to another tab.
                3. Finally, visualize both sets of data on a map.
            - Ensure that the final script runs all the steps seamlessly.
            **Deliverable**: A Python script that completes the entire task, from filtering the data to visualizing it on a map.
            """)

        with tab2:
            st.markdown("""
            ### Detailed Grading Breakdown
            #### 1. Library Imports (10 Points)
            - Checks if the required libraries are imported correctly.
            """)
            # Add "See More" expandable section
            with st.expander("See More"):
                st.markdown("""
            #### 2. Code Quality (20 Points)
            - **Descriptive Variable Names (5 Points)**:
                - Deducted if non-descriptive variable names are used (e.g., `x`, `y`).
            - **Spacing and Indentation (5 Points)**:
                - Deducted if improper spacing or indentation is found.
            - **Comments (5 Points)**:
                - Deducted if no comments are present to explain major steps.
            - **Code Organization (5 Points)**:
                - Deducted if code blocks are not logically separated with blank lines or functions.

            #### 3. Functionality (10 Points)
            - **JSON API Usage (5 Points)**:
                - Deducted if the JSON API is not used effectively.
            - **Function Encapsulation (5 Points)**:
                - Deducted if the functionality of Stage 1, Stage 2, and Stage 3 is not encapsulated into distinct functions.

            #### 4. Data Filtering (10 Points)
            - **Filter Data Below 25°C (5 Points)**:
                - Deducted if the filtering is incorrect or incomplete.
            - **Filter Data Above 25°C (5 Points)**:
                - Deducted if the filtering is incorrect or incomplete.

            #### 5. Data Mapping and Visualization (20 Points)
            - **Map Generation (5 Points)**:
                - Deducted if the map is not generated or displayed.
            - **Color-Coded Data Points (10 Points)**:
                - Deducted if data points are not color-coded correctly:
                    - Blue for "Below_25": 5 points
                    - Red for "Above_25": 5 points
            - **Accuracy of Coordinates (5 Points)**:
                - Deducted if the map does not accurately display the temperature data at the correct coordinates.

            #### 6. Excel File Grading (30 Points)
            - **Correct Sheets (10 Points)**:
                - Deducted if the Excel file does not include the "Below_25" and "Above_25" sheets.
            - **Data Accuracy (10 Points)**:
                - Deducted if the data in the sheets is incorrect or incomplete.
            - **File Format (10 Points)**:
                - Deducted if the file is not saved in the correct format or structure.
            """)

        # Step 3: Code Submission and Output
        st.header("Step 3: Run and Submit Your Code")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Step 4: Upload Files
        st.header("Step 4: Upload Your Outputs")
        uploaded_excel = st.file_uploader("Upload your Excel file", type=["xlsx"])
        uploaded_map = st.file_uploader("Upload your Map file (HTML or PNG)", type=["html", "png"])

        all_uploaded = all([uploaded_excel, uploaded_map])
        st.write("All files uploaded:", "✅ Yes" if all_uploaded else "❌ No")

        if all_uploaded:
            submit_button = st.button("Submit Assignment")

            if submit_button:
                try:
                    temp_dir = "temp_uploads"
                    os.makedirs(temp_dir, exist_ok=True)
                    excel_path = os.path.join(temp_dir, "uploaded_excel.xlsx")
                    map_path = os.path.join(temp_dir, "uploaded_map.html" if uploaded_map.type == "text/html" else "uploaded_map.png")

                    with open(excel_path, "wb") as f:
                        f.write(uploaded_excel.getvalue())
                    with open(map_path, "wb") as f:
                        f.write(uploaded_map.getvalue())

                    # Get only the numerical grade (0-100)
                    grade = grade_assignment(code_input, excel_path, map_path)
                    st.success(f"Your grade for Assignment 3: {grade}/100")

                    # Now update Google Sheets with the numerical grade only.
                    update_google_sheet(
                        full_name="",  # Update if needed
                        email="",      # Update if needed
                        student_id=student_id,
                        grade=grade,
                        current_assignment="assignment_3"
                    )

                except Exception as e:
                    st.error(f"An error occurred during submission: {e}")

        else:
            st.warning("Please upload all required files to proceed.")

if __name__ == "__main__":
    show()
