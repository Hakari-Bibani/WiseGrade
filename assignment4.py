import streamlit as st
import os
from grades.grade4 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 4: Image Analysis and Rectangle Detection")

    # Prevent submission if Assignment 3 is not submitted
    if "assignment3_submitted" not in st.session_state:
        st.session_state["assignment3_submitted"] = False

    if not st.session_state["assignment3_submitted"]:
        st.warning("You cannot submit Assignment 4 before submitting Assignment 3.")
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
            ### Objective
            The goal of this assignment is to perform image analysis and rectangle detection in Python. Students will use a provided thresholded image to detect rectangles and outline them in an output image.
            Detailed instructions will be provided here.
            """)
            # Placeholder for expandable details
            with st.expander("See More"):
                st.write("Assignment details will be provided here.")

        with tab2:
            st.markdown("""
            ### Grading Breakdown
            The grading criteria for this assignment will be provided here.
            """)
            # Placeholder for grading details
            with st.expander("See More"):
                st.write("Grading details will be provided here.")

        # Step 3: Assignment Submission
        st.header("Step 3: Submit Your Assignment")
        code_input = st.text_area("**Paste Your Code Here**", height=300)

        # Step 4: Upload Files
        st.header("Step 4: Upload Files")
        uploaded_threshold_image = st.file_uploader("Upload your thresholded image", type=["png", "jpg", "jpeg"])
        uploaded_rect_image = st.file_uploader("Upload your image with rectangles outlined", type=["png", "jpg", "jpeg"])

        # Step 5: Submit Button
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate required files
                if not uploaded_threshold_image:
                    st.error("Please upload the thresholded image.")
                    return
                if not uploaded_rect_image:
                    st.error("Please upload the image with rectangles outlined.")
                    return

                # Save uploaded files temporarily
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                # Save thresholded image
                threshold_image_path = os.path.join(temp_dir, "thresholded_image.png")
                with open(threshold_image_path, "wb") as f:
                    f.write(uploaded_threshold_image.getvalue())

                # Save rectangle image
                rect_image_path = os.path.join(temp_dir, "rectangles_image.png")
                with open(rect_image_path, "wb") as f:
                    f.write(uploaded_rect_image.getvalue())

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(code_input, threshold_image_path, rect_image_path)

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

