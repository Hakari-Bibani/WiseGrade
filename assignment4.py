import streamlit as st
import os
from grades.grade4 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    st.title("Assignment 4: Image Analysis and Rectangle Detection")

    # Prevent resubmission of Assignment 4 after another assignment
    if "assignment5_submitted" not in st.session_state:
        st.session_state["assignment5_submitted"] = False

    if st.session_state["assignment5_submitted"]:
        st.warning("You cannot resubmit Assignment 4 after submitting the next assignment.")
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
                st.error("Invalid Student ID. You must use the ID used for Assignment 3.")
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
            In this assignment, students will analyze an image to detect rectangles and visualize them. The task is broken into three stages, with each stage encapsulating a specific function. By the end of the assignment, students will merge the functions into one script to complete the task efficiently.
            """)
            # Placeholder for "See More" text
            with st.expander("See More"):
                st.markdown("Assignment-specific instructions will go here.")

        with tab2:
            st.markdown("""
            ### Detailed Grading Breakdown
            Detailed grading criteria for image analysis and rectangle detection will be provided here.
            """)
            with st.expander("See More"):
                st.markdown("Grading details for each stage of the assignment.")

        # Step 3: Assignment Submission
        st.header("Step 3: Submit Your Assignment")

        # Code Input
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Rectangle Coordinates Input
        st.header("Step 4: Enter Rectangle Coordinates")
        rectangle_coordinates = st.text_area(
            "Paste Rectangle Coordinates (Top-Left and Bottom-Right) Here",
            height=150
        )

        # Upload Thresholded Image
        st.header("Step 5: Upload Your Thresholded Image")
        uploaded_thresholded_image = st.file_uploader("Upload your thresholded image file", type=["png", "jpg", "jpeg"])

        # Upload Image with Rectangles
        st.header("Step 6: Upload Image with Rectangles Outlined")
        uploaded_outlined_image = st.file_uploader("Upload your image with rectangles outlined", type=["png", "jpg", "jpeg"])

        # Submit Button
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                # Validate required files
                if not uploaded_thresholded_image:
                    st.error("Please upload a thresholded image file.")
                    return
                if not uploaded_outlined_image:
                    st.error("Please upload an image with rectangles outlined.")
                    return

                # Save uploaded files temporarily
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                # Save thresholded image
                thresholded_image_path = os.path.join(temp_dir, "thresholded_image.png")
                with open(thresholded_image_path, "wb") as f:
                    f.write(uploaded_thresholded_image.getvalue())

                # Save outlined image
                outlined_image_path = os.path.join(temp_dir, "outlined_image.png")
                with open(outlined_image_path, "wb") as f:
                    f.write(uploaded_outlined_image.getvalue())

                # Parse rectangle coordinates
                try:
                    student_coordinates = []
                    for line in rectangle_coordinates.splitlines():
                        line = line.strip()
                        if not line or line.startswith("Rectangle Coordinates"):  # Skip invalid lines or headers
                            continue
                        coords = line.split(":")[1].strip()  # Extract coordinates after "Rectangle X:"
                        top_left, bottom_right = coords.split(", Bottom-Right ")
                        top_left = tuple(map(int, top_left.replace("Top-Left (", "").replace(")", "").split(",")))
                        bottom_right = tuple(map(int, bottom_right.replace("(", "").replace(")", "").split(",")))
                        student_coordinates.append((top_left, bottom_right))
                except Exception as e:
                    st.error(f"Invalid input format for rectangle coordinates: {e}")
                    return

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(
                    code_input,
                    student_coordinates,
                    thresholded_image_path,
                    outlined_image_path
                )

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
