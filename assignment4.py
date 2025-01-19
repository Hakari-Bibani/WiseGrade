import streamlit as st
import os
from grades.grade4 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 4: Image Analysis and Rectangle Detection")

    # Sidebar Navigation
    with st.sidebar:
        st.subheader("Assignment Navigation")
        st.info("You are currently on Assignment 4.")

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
        # Tabs for Assignment and Grading Details
        st.header("Step 2: Review Assignment Details")
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("### Assignment Details will be added here.")

        with tab2:
            st.markdown("### Grading Details will be added here.")

        # Step 3: Assignment Submission
        st.header("Step 3: Submit Your Assignment")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)
        rectangle_coords = st.text_area("**📋 Paste Detected Rectangle Coordinates Here**", height=100)
        uploaded_threshold_image = st.file_uploader("Upload your thresholded image", type=["png", "jpg", "jpeg"])
        uploaded_rectangle_image = st.file_uploader("Upload your outlined image", type=["png", "jpg", "jpeg"])

        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                if not uploaded_threshold_image:
                    st.error("Please upload a thresholded image.")
                    return
                if not uploaded_rectangle_image:
                    st.error("Please upload an image with rectangles outlined.")
                    return

                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                threshold_image_path = os.path.join(temp_dir, "thresholded_image.png")
                with open(threshold_image_path, "wb") as f:
                    f.write(uploaded_threshold_image.getvalue())

                rectangle_image_path = os.path.join(temp_dir, "outlined_image.png")
                with open(rectangle_image_path, "wb") as f:
                    f.write(uploaded_rectangle_image.getvalue())

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(
                    code_input, rectangle_coords, threshold_image_path, rectangle_image_path
                )

                # Display grades
                st.success(f"Your total grade: {total_grade}/100")
                for category, score in grading_breakdown.items():
                    st.write(f"{category}: {score} points")

                # Update grades in Google Sheets
                update_google_sheet(
                    full_name="",  # Fill with the student's full name if available
                    email="",      # Fill with the student's email if available
                    student_id=student_id,
                    grade=total_grade,
                    current_assignment="assignment_4"
                )

            except Exception as e:
                st.error(f"An error occurred during submission: {e}")

