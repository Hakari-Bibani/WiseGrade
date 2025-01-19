import streamlit as st
import os
from grades.grade4 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 4: Image Analysis and Rectangle Detection in Python")

    # Prevent resubmission of Assignment 4 if Assignment 3 is not submitted
    if "assignment3_submitted" not in st.session_state:
        st.session_state["assignment3_submitted"] = False

    if not st.session_state["assignment3_submitted"]:
        st.warning("You cannot access Assignment 4 unless you have submitted Assignment 3.")
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
                st.error("Invalid Student ID. Please enter a valid ID from Assignment 3.")
                st.session_state["verified"] = False

        except Exception as e:
            st.error(f"An error occurred while verifying Student ID: {e}")
            st.session_state["verified"] = False

    if st.session_state.get("verified", False):
        # Add Tabs for Assignment Details and Grading Details
        st.header("Step 2: Review Assignment Details")
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("""
            ### Assignment Details
            _Provide detailed instructions here for students. This can include:
            - The goal of the assignment.
            - Step-by-step breakdown of tasks.
            - Example input/output formats._
            """)

        with tab2:
            st.markdown("""
            ### Grading Details
            _Provide a detailed grading rubric here. Break down the points for:
            - Code structure and quality.
            - Functionality and correctness.
            - Proper submission of required files._
            """)

        # Step 3: Assignment Submission
        st.header("Step 3: Submit Your Assignment")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Step 4: Upload Files
        st.header("Step 4: Upload Images")
        uploaded_thresh_image = st.file_uploader("Upload your thresholded image", type=["png", "jpg", "jpeg"])
        uploaded_outlined_image = st.file_uploader("Upload your image with rectangles outlined", type=["png", "jpg", "jpeg"])

        # Step 5: Submit Button
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate required files
                if not uploaded_thresh_image:
                    st.error("Please upload the thresholded image.")
                    return
                if not uploaded_outlined_image:
                    st.error("Please upload the outlined image.")
                    return

                # Save uploaded files temporarily
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                # Save thresholded image
                thresh_image_path = os.path.join(temp_dir, "thresholded_image.png")
                with open(thresh_image_path, "wb") as f:
                    f.write(uploaded_thresh_image.getvalue())

                # Save outlined image
                outlined_image_path = os.path.join(temp_dir, "outlined_image.png")
                with open(outlined_image_path, "wb") as f:
                    f.write(uploaded_outlined_image.getvalue())

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(code_input, thresh_image_path, outlined_image_path)

                # Display total grade only
                st.success(f"Your total grade: {total_grade}/100")

                # Update Google Sheets with grade
                update_google_sheet(
                    full_name="",  # Fill with the student's full name if available
                    email="",      # Fill with the student's email if available
                    student_id=student_id,
                    grade=total_grade,
                    current_assignment="assignment_4"
                )

            except Exception as e:
                st.error(f"An error occurred during submission: {e}")

if __name__ == "__main__":
    show()

