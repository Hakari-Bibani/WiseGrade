import streamlit as st
import os
import cv2
import numpy as np
from grades.grade4 import grade_assignment
from Record.google_sheet import update_google_sheet

def grade_thresholded_image(uploaded_image_path):
    """
    Grade thresholded image by counting detected rectangles
    Returns 0-20 points based on number of rectangles detected
    """
    try:
        # Read the uploaded image in grayscale
        image = cv2.imread(uploaded_image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return 0, "Failed to read uploaded image"
            
        # Ensure image is binary/thresholded
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours in the binary image
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Count rectangles (filter contours that are roughly rectangular)
        rectangle_count = 0
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Calculate contour area and bounding rectangle area
            contour_area = cv2.contourArea(contour)
            rect_area = w * h
            
            # If contour area is similar to rectangle area, it's likely a rectangle
            if contour_area > 0 and rect_area > 0:
                area_ratio = contour_area / rect_area
                if area_ratio > 0.85:  # Threshold for rectangle detection
                    rectangle_count += 1
        
        # Calculate grade based on rectangle count
        if rectangle_count == 14:
            return 20, f"Found all 14 rectangles: 20 points"
        elif rectangle_count > 7:
            points = int(20 * (rectangle_count / 14))
            return points, f"Found {rectangle_count}/14 rectangles: {points} points"
        else:
            return 0, f"Found only {rectangle_count} rectangles: 0 points"
            
    except Exception as e:
        return 0, f"Error processing image: {str(e)}"

def grade_outlined_image(uploaded_path, correct_path="grades/correct_files/correct_outlined.png"):
    """
    Grade outlined image by comparing with correct image
    Returns 4 points if matches, 0 if not
    """
    try:
        # Read both images
        uploaded = cv2.imread(uploaded_path)
        correct = cv2.imread(correct_path)
        
        if uploaded is None or correct is None:
            return 0, "Failed to read one or both images"
            
        # Check if images have same dimensions
        if uploaded.shape != correct.shape:
            return 0, "Image dimensions don't match reference image"
            
        # Compare images
        difference = cv2.absdiff(uploaded, correct)
        difference_sum = np.sum(difference)
        
        # Allow for small differences due to compression
        if difference_sum < 1000:  # Threshold for image comparison
            return 4, "Image matches reference: 4 points"
        else:
            return 0, "Image doesn't match reference: 0 points"
            
    except Exception as e:
        return 0, f"Error comparing images: {str(e)}"

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
            saved_ids = [row[2] for row in worksheet.get_all_values()[1:]]  # Student ID in 3rd column

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
        # Assignment Details
        st.header("Step 2: Review Assignment Details")
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("""
            ### Objective
            In this assignment, students will analyze an image to detect rectangles and visualize them. 
            The task is broken into three stages, with each stage encapsulating a specific function.
            """)
            with st.expander("See More"):
                st.markdown("Assignment-specific instructions will go here.")

        with tab2:
            st.markdown("""
            ### Grading Breakdown
            - Library Imports: 10 points
            - Code Quality: 10 points
            - Rectangle Coordinates: 56 points
            - Thresholded Image: 20 points
            - Image with Rectangles Outlined: 4 points
            """)

        # Assignment Submission
        st.header("Step 3: Submit Your Assignment")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Rectangle Coordinates Input
        st.header("Step 4: Enter Rectangle Coordinates")
        rectangle_coordinates = st.text_area(
            "Paste Rectangle Coordinates (Top-Left and Bottom-Right) Here",
            height=150
        )

        # Upload Images
        st.header("Step 5: Upload Your Thresholded Image")
        uploaded_thresholded_image = st.file_uploader("Upload your thresholded image file", type=["png", "jpg", "jpeg"])

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

                # Create temporary directory for uploads
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                # Save and process thresholded image
                thresholded_image_path = os.path.join(temp_dir, "thresholded_image.png")
                with open(thresholded_image_path, "wb") as f:
                    f.write(uploaded_thresholded_image.getvalue())

                # Save and process outlined image
                outlined_image_path = os.path.join(temp_dir, "outlined_image.png")
                with open(outlined_image_path, "wb") as f:
                    f.write(uploaded_outlined_image.getvalue())

                # Grade thresholded image
                thresholded_image_grade, thresh_message = grade_thresholded_image(thresholded_image_path)
                st.write(f"Thresholded Image: {thresh_message}")

                # Grade outlined image
                outlined_image_grade, outline_message = grade_outlined_image(outlined_image_path)
                st.write(f"Outlined Image: {outline_message}")

                # Grade rectangle coordinates
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
                    rectangle_grade = sum(1 for i, val in enumerate(student_values) 
                                       if i < len(correct_values) and val == correct_values[i])
                except Exception as e:
                    st.error(f"Invalid rectangle coordinates format: {e}")
                    rectangle_grade = 0

                # Calculate final grade
                total_grade, grading_breakdown = grade_assignment(
                    code_input, 
                    rectangle_grade,
                    thresholded_image_grade,
                    outlined_image_grade
                )

                # Display results
                st.success(f"Your total grade: {total_grade}/100")
                st.header("Grading Breakdown")
                for criterion, score in grading_breakdown.items():
                    st.write(f"**{criterion}:** {score} points")

                # Update Google Sheets
                update_google_sheet(
                    full_name="",
                    email="",
                    student_id=student_id,
                    grade=total_grade,
                    current_assignment="assignment_4"
                )

                # Clean up temporary files
                try:
                    os.remove(thresholded_image_path)
                    os.remove(outlined_image_path)
                    os.rmdir(temp_dir)
                except Exception as e:
                    st.warning(f"Cleanup warning: {e}")

            except Exception as e:
                st.error(f"An error occurred during submission: {e}")

if __name__ == "__main__":
    show()
