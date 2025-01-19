import streamlit as st
import os
from grades.grade4 import grade_assignment

def show():
    st.title("Assignment 4: Image Analysis and Rectangle Detection")

    # Prevent resubmission of Assignment 4
    if "assignment4_submitted" not in st.session_state:
        st.session_state["assignment4_submitted"] = False

    if st.session_state["assignment4_submitted"]:
        st.warning("You cannot resubmit Assignment 4 after submitting it.")
        return

    # Step 1: Validate Student ID (keeping the existing validation logic)
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Enter Your Student ID")
    verify_button = st.button("Verify Student ID")

    if verify_button:
        try:
            # Your existing verification code here
            st.session_state["verified"] = True  # For testing, you might want to modify this logic
        except Exception as e:
            st.error(f"An error occurred while verifying Student ID: {e}")
            st.session_state["verified"] = False

    if st.session_state.get("verified", False):
        # Assignment Details and Grading Details
        st.header("Step 2: Review Assignment Details")
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("""
            ### Assignment 4: Image Analysis and Rectangle Detection
            
            #### Requirements:
            1. Import required libraries:
                - OpenCV (cv2) / Pillow (PIL) / Scikit-Image / ImageAI
                - NumPy / SciPy / TensorFlow / PyTorch
                - Matplotlib / Plotly / Seaborn / Pillow
                
            2. Code Quality:
                - Use descriptive variable names
                - Maintain proper spacing
                - Include comments explaining major steps
                - Organize code with logical separation
                
            3. Rectangle Detection:
                - Detect and outline 14 rectangles in the provided image
                - Provide accurate coordinates for each rectangle
                
            4. Image Processing:
                - Submit a properly thresholded image
                - Submit an image with correctly outlined rectangles
            """)

        with tab2:
            st.markdown("""
            ### Grading Breakdown:
            
            1. Library Imports (15 Points)
                - Image processing library (5 points)
                - Numerical processing library (5 points)
                - Visualization library (5 points)
                
            2. Code Quality (20 Points)
                - Variable naming (5 points)
                - Spacing (5 points)
                - Comments (5 points)
                - Code organization (5 points)
                
            3. Rectangle Coordinates (28 Points)
                - 2 points for each correctly detected rectangle
                
            4. Thresholded Image (20 Points)
                - Accuracy in rectangle detection
                
            5. Outlined Image (17 Points)
                - Quality of rectangle outlining
            """)

        # Step 3: Assignment Submission
        st.header("Step 3: Submit Your Assignment")

        # Code submission
        st.subheader("Submit Your Code")
        code_input = st.text_area(
            "📝 Paste your complete Python code here",
            height=300,
            help="Include all imports and full implementation"
        )

        # Rectangle coordinates
        st.subheader("Submit Rectangle Coordinates")
        st.markdown("""
        Format example:
        ```
        Rectangle 1: Top-Left (x1, y1), Bottom-Right (x2, y2)
        Rectangle 2: Top-Left (x1, y1), Bottom-Right (x2, y2)
        ```
        """)
        rectangle_coords = st.text_area(
            "📋 Paste the detected rectangle coordinates",
            height=200
        )

        # Image uploads
        st.subheader("Submit Your Images")
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_threshold_image = st.file_uploader(
                "Upload thresholded image",
                type=["png", "jpg", "jpeg"],
                help="Upload your binary/thresholded image showing detected rectangles"
            )

        with col2:
            uploaded_rectangle_image = st.file_uploader(
                "Upload outlined image",
                type=["png", "jpg", "jpeg"],
                help="Upload your image with rectangles outlined in color"
            )

        # Submit button
        submit_button = st.button("Submit Assignment")

        if submit_button:
            try:
                if not all([code_input.strip(), rectangle_coords.strip(), 
                           uploaded_threshold_image, uploaded_rectangle_image]):
                    st.error("Please provide all required submissions.")
                    return

                # Save uploaded files
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)

                threshold_image_path = os.path.join(temp_dir, "thresholded_image.png")
                rectangle_image_path = os.path.join(temp_dir, "outlined_image.png")

                with open(threshold_image_path, "wb") as f:
                    f.write(uploaded_threshold_image.getvalue())
                with open(rectangle_image_path, "wb") as f:
                    f.write(uploaded_rectangle_image.getvalue())

                # Paths to correct files
                correct_threshold_path = "correct_files/correct_thresholded_image.png"
                correct_outline_path = "correct_files/correct_outlined_image.png"

                # Grade the assignment
                total_grade, grading_breakdown = grade_assignment(
                    code_input,
                    rectangle_coords,
                    threshold_image_path,
                    rectangle_image_path,
                    correct_threshold_path,
                    correct_outline_path
                )

                # Display results
                st.success(f"Total Grade: {total_grade}/100")
                
                # Display detailed breakdown
                st.subheader("Grading Breakdown")
                for category, details in grading_breakdown.items():
                    st.write(f"**{category.replace('_', ' ')}:**")
                    st.json(details)

                # Update submission status
                st.session_state["assignment4_submitted"] = True

                # Clean up temporary files
                try:
                    os.remove(threshold_image_path)
                    os.remove(rectangle_image_path)
                except:
                    pass

            except Exception as e:
                st.error(f"An error occurred during submission: {e}")

if __name__ == "__main__":
    show()
