import streamlit as st
import os
from grades.grade3 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 3: Advanced Earthquake Data Analysis")

    # Prevent resubmission
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
        # Step 2: Assignment Submission
        st.header("Step 2: Submit Your Assignment")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Step 3: Upload Files
        st.header("Step 3: Upload Your HTML and Excel Files")
        uploaded_html = st.file_uploader("Upload your HTML file (Map)", type=["html"])
        uploaded_excel = st.file_uploader("Upload your Excel file (Google Sheet)", type=["xlsx"])

        # Step 4: Submit Button
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate required files
                if not uploaded_html:
                    st.error("Please upload an HTML file for the interactive map.")
                    return
                if not uploaded_excel:
                    st.error("Please upload your Excel file.")
                    return

                # Save uploaded files temporarily
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
                total_grade, grading_breakdown = grade_assignment(code_input, html_path, excel_path)

                # Display grades
                st.success(f"Your total grade: {total_grade}/100")
                st.subheader("Detailed Grading Breakdown:")
                for category, points in grading_breakdown.items():
                    st.write(f"**{category}:** {points} points")

                # Update Google Sheets with grade
                update_google_sheet(
                    full_name="",  # Fill with the student's full name if available
                    email="",      # Fill with the student's email if available
                    student_id=student_id,
                    grade=total_grade,
                    current_assignment="assignment_3"
                )

                # Mark as submitted
                st.session_state["assignment3_submitted"] = True

            except Exception as e:
                st.error(f"An error occurred during submission: {e}")

if __name__ == "__main__":
   
