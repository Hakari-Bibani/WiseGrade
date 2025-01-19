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
            ### Objective:
            In this assignment, you will use Python image processing libraries to analyze a black-and-white image, detect rectangular shapes, and determine the coordinates of each rectangle.
            """)
            with st.expander("See More"):
                st.markdown("""
                #### Instructions:
                1. **Set Up Your Environment:**
                   - Open a new Google Colab notebook.
                   - Import the necessary libraries:
                     - `cv2` (OpenCV) for image processing.
                     - `numpy` for numerical operations.
                     - `matplotlib` for displaying images.

                2. **Load the Image:**
                   - Download the provided image and upload it to Google Colab.
                   - Load the image using OpenCV.

                3. **Convert the Image to Grayscale and Apply Thresholding:**
                   - Convert the image to grayscale.
                   - Use binary thresholding to make it easier to detect the rectangular shapes. This will turn the rectangles into clear white shapes against a black background.

                4. **Detect Contours:**
                   - Use OpenCV’s `findContours` function to detect all contours in the image.
                   - Filter out contours that are not rectangular shapes.

                5. **Filter and Identify Rectangles:**
                   - For each contour, approximate its shape using `cv2.approxPolyDP`.
                   - If the contour has four points, consider it a rectangle.
                   - Calculate the bounding box coordinates of each rectangle using `cv2.boundingRect`.

                6. **Extract and Print the Coordinates:**
                   - For each detected rectangle, print the top-left and bottom-right coordinates.
                   - Display the original image with the rectangles outlined for verification.
                """)

        with tab2:
            st.markdown("""
            ### Detailed Grading Breakdown
            """)
            with st.expander("See More"):
                st.markdown("""
                1. **Library Imports (20 Points)**
                   - Checks if the required libraries are imported correctly.

                2. **Code Quality (20 Points)**
                   - **Descriptive Variable Names (5 Points):**
                     - Deducted if non-descriptive variable names are used (e.g., x, y).
                   - **Spacing and Indentation (5 Points):**
                     - Deducted if improper spacing or indentation is found.
                   - **Comments (5 Points):**
                     - Deducted if no comments are present to explain major steps.
                   - **Code Organization (5 Points):**
                     - Deducted if code blocks are not logically separated with blank lines or functions.

                3. **Rectangle Coordinates (30 Points)**
                   - You can paste them as (for instance):
                     ```
                     Rectangle 1: Top-Left (1678, 1705), Bottom-Right (8061, 7612)
                     Rectangle 2: Top-Left (459, 9805), Bottom-Right (728, 6712)
                     ```
                   - Or:
                     ```
                     (1374, 1605), (7878, 3705), (9678, 4705), (4608, 3705), ….
                     ```

                4. **Upload Thresholded Image (15 Points):**
                   - Upload file as PNG.

                5. **Upload Image with Rectangles Outlined (15 Points):**
                   - Upload file as PNG.
                """)

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
                    correct_values = [
                        1655, 1305, 2021, 1512, 459, 1305, 825, 1512,
                        2051, 1305, 2417, 1512, 1257, 1305, 1623, 1512,
                        857, 1305, 1223, 1512, 63, 1305, 429, 1512,
                        157, 1050, 398, 1122, 351, 869, 592, 941,
                        624, 744, 865, 816, 888, 646, 1129, 718,
                        1069, 492, 1311, 564, 1338, 360, 1579, 432,
                        64, 231, 800, 506, 2103, 166, 2344, 239
                    ]
                    student_values = [
                        int(value) for line in rectangle_coordinates.splitlines()
                        for value in line.replace("Top-Left (", "").replace("Bottom-Right (", "")
                        .replace(")", "").replace(",", " ").split()
                        if value.isdigit()
                    ]
                    rectangle_grade = sum(1 for i, val in enumerate(student_values) if i < len(correct_values) and val == correct_values[i])
                except Exception as e:
                    st.error(f"Invalid input format for rectangle coordinates: {e}")
                    return

                # Grade Thresholded Image
                thresholded_image_grade = 0
                try:
                    from PIL import Image
                    image = Image.open(thresholded_image_path).convert("L")  # Convert to grayscale
                    if image:
                        thresholded_image_grade = 5  # Award 5 points for a valid black-and-white image
                except Exception as e:
                    st.error(f"Error processing thresholded image: {e}")

                # Grade Outlined Image
                outlined_image_grade = 0
                try:
                    # Simplified check for outlined image validation
                    outlined_image_grade = 5  # Assume correct image comparison logic here
                except Exception as e:
                    st.error(f"Error processing outlined image: {e}")

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(
                    code_input,
                    rectangle_grade,
                    thresholded_image_grade,
                    outlined_image_grade
                )

                # Display total grade and detailed breakdown
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
