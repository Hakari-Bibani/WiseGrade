import streamlit as st
import os
from grades.grade4 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 4: Image Analysis and Rectangle Detection")

    # Prevent access to Assignment 4 if Assignment 3 was not submitted
    if "assignment3_submitted" not in st.session_state:
        st.session_state["assignment3_submitted"] = False

    if not st.session_state["assignment3_submitted"]:
        st.warning("You must submit Assignment 3 before accessing Assignment 4.")
        return

    # Validate Student ID
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
            st.markdown("""### Assignment 4: Image Analysis and Rectangle Detection
            **Objective**: Analyze images to detect rectangular objects and apply thresholding for preprocessing. 
            **Tasks**:
            - Apply thresholding to the provided image.
            - Detect rectangles in the processed image.
            - Outline detected rectangles and save the output.
            """)

        with tab2:
            st.markdown("""### Detailed Grading Breakdown
            - Thresholding accuracy: 30 points
            - Rectangle detection: 40 points
            - Output clarity and file formatting: 30 points
            Total: 100 points
            """)

        # Step 3: Assignment Submission
        st.header("Step 3: Submit Your Assignment")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Step 4: Upload Thresholded Image
        st.header("Step 4: Upload Your Thresholded Image")
        uploaded_thresh_image = st.file_uploader("Upload the thresholded image", type=["png", "jpg", "jpeg"])

        # Step 5: Upload Image with Rectangles Outlined
        st.header("Step 5: Upload Your Image with Rectangles Outlined")
        uploaded_rect_image = st.file_uploader("Upload the image with rectangles outlined", type=["png", "jpg", "jpeg"])

        # Submit Button
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate required files
                if not uploaded_thresh_image:
                    st.error("Please upload the thresholded image.")
                    return
                if not uploaded_rect_image:
                    st.error("Please upload the image with rectangles outlined.")
                    return

                # Save uploaded files temporarily
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                # Save thresholded image
                thresh_image_path = os.path.join(temp_dir, "thresholded_image.png")
                with open(thresh_image_path, "wb") as f:
                    f.write(uploaded_thresh_image.getvalue())

                # Save rectangle-outlined image
                rect_image_path = os.path.join(temp_dir, "rectangles_image.png")
                with open(rect_image_path, "wb") as f:
                    f.write(uploaded_rect_image.getvalue())

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(code_input, thresh_image_path, rect_image_path)

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
