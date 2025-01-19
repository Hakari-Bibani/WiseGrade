import os
from PIL import Image

def grade_assignment(code_input, thresh_image_path, outlined_image_path):
    """
    Grades the Assignment 4 submission.

    Args:
        code_input (str): The code submitted by the student.
        thresh_image_path (str): Path to the uploaded thresholded image.
        outlined_image_path (str): Path to the uploaded outlined image.

    Returns:
        tuple: Total grade (int) and grading breakdown (dict).
    """
    # Initialize total grade and grading breakdown
    total_grade = 0
    grading_breakdown = {
        "Code Quality": 0,
        "Threshold Image Validation": 0,
        "Outlined Image Validation": 0,
    }

    # Step 1: Evaluate the Code
    try:
        # Example: Check if the code contains required functions or libraries
        if "cv2" in code_input or "PIL" in code_input:
            grading_breakdown["Code Quality"] = 30  # Assign full marks for code containing required libraries
        else:
            grading_breakdown["Code Quality"] = 15  # Partial marks if libraries are missing

        total_grade += grading_breakdown["Code Quality"]
    except Exception as e:
        print(f"Error grading code: {e}")

    # Step 2: Validate Threshold Image
    try:
        if os.path.exists(thresh_image_path):
            thresh_image = Image.open(thresh_image_path)

            # Example: Check if the image is grayscale
            if thresh_image.mode == "L":
                grading_breakdown["Threshold Image Validation"] = 30
            else:
                grading_breakdown["Threshold Image Validation"] = 15

            total_grade += grading_breakdown["Threshold Image Validation"]
    except Exception as e:
        print(f"Error validating threshold image: {e}")

    # Step 3: Validate Outlined Image
    try:
        if os.path.exists(outlined_image_path):
            outlined_image = Image.open(outlined_image_path)

            # Example: Check if the image contains rectangles (placeholder logic)
            # In real-world scenarios, use a library like OpenCV for rectangle detection.
            if "Rectangle Detected" in outlined_image.info.get("description", ""):  # Placeholder logic
                grading_breakdown["Outlined Image Validation"] = 40
            else:
                grading_breakdown["Outlined Image Validation"] = 20

            total_grade += grading_breakdown["Outlined Image Validation"]
    except Exception as e:
        print(f"Error validating outlined image: {e}")

    # Return total grade and breakdown
    return total_grade, grading_breakdown
