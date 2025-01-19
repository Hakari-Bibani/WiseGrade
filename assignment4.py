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
        st.warning("You must submit Assignment 3 before attempting Assignment 4.")
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
            In this assignment, students will analyze an image and detect rectangles using Python. The task involves:
            - Thresholding the image to isolate rectangles.
            - Detecting and outlining rectangles in the image.
            - Verifying the coordinates of the detected rectangles.
            """)
            with st.expander("See More"):
                st.markdown("""
            ### Detailed Instructions
            1. **Threshold the Image**:
                - Use OpenCV, Pillow, or Scikit-Image to threshold the provided image.
                - Save the thresholded image for submission.
            2. **Detect Rectangles**:
                - Use contour detection or edge detection to identify rectangles in the image.
                - Outline the detected rectangles and save the resulting image.
            3. **Verify Coordinates**:
                - Compare the detected rectangle coordinates with the correct coordinates provided in the grading details.
            """)

        with tab2:
            st.markdown("""
            ### Grading Breakdown
            #### 1. Library Imports (15 Points)
            - OpenCV, Pillow, Scikit-Image, or ImageAI: 5 points
            - NumPy, SciPy, TensorFlow, or PyTorch: 5 points
            - Matplotlib, Plotly, Seaborn, or Pillow: 5 points
            """)
            with st.expander("See More"):
                st.markdown("""
            #### 2. Code Quality (20 Points)
            - **Variable Naming**: 5 points
            - **Spacing**: 5 points
            - **Comments**: 5 points
            - **Code Organization**: 5 points

            #### 3. Rectangle Coordinates (28 Points)
            - Each rectangle's coordinates are compared against the correct values. Points are awarded for accuracy.

            #### 4. Thresholded Image (20 Points)
            - The number of rectangles in the thresholded image is verified.

            #### 5. Outlined Rectangles (17 Points)
            - The presence of outlined rectangles in the uploaded image is verified.
            """)

        # Step 3: Assignment Submission
        st.header("Step 3: Submit Your Assignment")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Step 4: Upload Files
        st.header("Step 4: Upload Your Images")
        uploaded_threshold = st.file_uploader("Upload Thresholded Image", type=["png", "jpg", "jpeg"])
        uploaded_outlined = st.file_uploader("Upload Image with Rectangles Outlined", type=["png", "jpg", "jpeg"])

        # Step 5: Submit Button
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate required files
                if not uploaded_threshold:
                    st.error("Please upload the thresholded image.")
                    return
                if not uploaded_outlined:
                    st.error("Please upload the image with outlined rectangles.")
                    return

                # Save uploaded files temporarily
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                # Save thresholded image
                threshold_path = os.path.join(temp_dir, "thresholded_image.png")
                with open(threshold_path, "wb") as f:
                    f.write(uploaded_threshold.getvalue())

                # Save outlined image
                outlined_path = os.path.join(temp_dir, "outlined_image.png")
                with open(outlined_path, "wb") as f:
                    f.write(uploaded_outlined.getvalue())

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(code_input, threshold_path, outlined_path)

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
