import streamlit as st
import os
from grades.grade4 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 4: Image Analysis and Rectangle Detection in Python")

    # Prevent resubmission of Assignment 4 after Assignment 5 submission
    if "assignment5_submitted" not in st.session_state:
        st.session_state["assignment5_submitted"] = False

    if st.session_state["assignment5_submitted"]:
        st.warning("You cannot resubmit Assignment 4 after submitting Assignment 5.")
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
                st.error("Invalid Student ID. Please enter a valid ID used in Assignment 3.")
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
            ### Objective
            This assignment involves analyzing an image, detecting rectangles, and providing their coordinates. You will also visualize the rectangles on the image and upload both the thresholded image and the outlined image for validation.
            """)

        with tab2:
            st.markdown("""
            ### Grading Criteria
            - **Rectangle Detection Accuracy (50 Points)**: Correctly detect all rectangles in the image.
            - **Thresholded Image Quality (25 Points)**: Ensure the thresholded image is clear and appropriate for rectangle detection.
            - **Outlined Image Accuracy (25 Points)**: Ensure all rectangles are outlined correctly and visible.
            """)

        # Step 3: Assignment Submission
        st.header("Step 3: Submit Your Assignment")

        # Code submission
        code_input = st.text_area("**\U0001F4DD Paste Your Code Here**", height=300)

        # Rectangle coordinates input
        st.header("Step 4: Enter Rectangle Coordinates")
        coordinates_input = st.text_area(
            "Enter Rectangle Coordinates (Top-Left and Bottom-Right)", height=200
        )

        # File uploads
        st.header("Step 5: Upload Files")
        uploaded_threshold = st.file_uploader("Upload your Thresholded Image", type=["png", "jpg", "jpeg"])
        uploaded_outlined = st.file_uploader("Upload your Outlined Image", type=["png", "jpg", "jpeg"])

        # Submit button
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate required files
                if not uploaded_threshold:
                    st.error("Please upload your thresholded image.")
                    return
                if not uploaded_outlined:
                    st.error("Please upload your outlined image.")
                    return

                # Save uploaded files temporarily
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                # Save thresholded image
                threshold_path = os.path.join(temp_dir, "uploaded_threshold.png")
                with open(threshold_path, "wb") as f:
                    f.write(uploaded_threshold.getvalue())

                # Save outlined image
                outlined_path = os.path.join(temp_dir, "uploaded_outlined.png")
                with open(outlined_path, "wb") as f:
                    f.write(uploaded_outlined.getvalue())

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(
                    code_input, coordinates_input, threshold_path, outlined_path
                )

                # Display total grade
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
