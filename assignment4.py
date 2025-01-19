import streamlit as st
import os
from grades.grade4 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 4: Image Analysis and Rectangle Detection in Python")

    # Prevent resubmission of Assignment 4 if not verified from Assignment 3
    if "assignment3_verified" not in st.session_state:
        st.session_state["assignment3_verified"] = False

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
                st.session_state["assignment3_verified"] = True
            else:
                st.error("Invalid Student ID. Make sure you submitted Assignment 3.")
                st.session_state["assignment3_verified"] = False

        except Exception as e:
            st.error(f"An error occurred while verifying Student ID: {e}")
            st.session_state["assignment3_verified"] = False

    if st.session_state.get("assignment3_verified", False):
        # Tabs for Assignment Details and Grading Details
        st.header("Step 2: Review Assignment Details")
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("### Assignment Details")
            st.markdown("Provide the detailed description here.")  # Placeholder for your text

        with tab2:
            st.markdown("### Grading Breakdown")
            st.markdown("Provide the grading details here.")  # Placeholder for your text

        # Step 3: Assignment Submission
        st.header("Step 3: Submit Your Assignment")
        code_input = st.text_area("**\U0001F4DD Paste Your Code Here**", height=300)

        # Step 4: Enter Rectangle Coordinates
        st.header("Step 4: Enter Rectangle Coordinates")
        top_left = st.text_input("Top-Left Coordinates (format: x,y)")
        bottom_right = st.text_input("Bottom-Right Coordinates (format: x,y)")

        # Step 5: Upload Files
        st.header("Step 5: Upload Your Files")
        uploaded_threshold_image = st.file_uploader("Upload Thresholded Image", type=["png", "jpg", "jpeg"])
        uploaded_outlined_image = st.file_uploader("Upload Image with Rectangles Outlined", type=["png", "jpg", "jpeg"])

        # Step 6: Submit Button
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate required fields
                if not uploaded_threshold_image:
                    st.error("Please upload a thresholded image.")
                    return
                if not uploaded_outlined_image:
                    st.error("Please upload an outlined image.")
                    return

                # Save uploaded files temporarily
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                threshold_image_path = os.path.join(temp_dir, "threshold_image.png")
                with open(threshold_image_path, "wb") as f:
                    f.write(uploaded_threshold_image.getvalue())

                outlined_image_path = os.path.join(temp_dir, "outlined_image.png")
                with open(outlined_image_path, "wb") as f:
                    f.write(uploaded_outlined_image.getvalue())

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(
                    code_input, threshold_image_path, outlined_image_path, top_left, bottom_right
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
