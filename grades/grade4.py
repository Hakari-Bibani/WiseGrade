import os

def grade_assignment(code_input, rectangle_coords, threshold_image_path, rectangle_image_path):
    """
    Grades the Assignment 4 submission.

    Args:
        code_input (str): The code submitted by the student.
        rectangle_coords (str): The detected rectangle coordinates submitted by the student.
        threshold_image_path (str): Path to the thresholded image uploaded by the student.
        rectangle_image_path (str): Path to the image with rectangles outlined uploaded by the student.

    Returns:
        tuple: Total grade (int) and detailed grading breakdown (dict).
    """
    total_grade = 0
    grading_breakdown = {}

    # 1. Code Quality (30 points)
    try:
        if len(code_input.strip()) > 0:
            # Check for essential components in the code (e.g., imports, functions)
            if "cv2" in code_input and "findContours" in code_input and "drawContours" in code_input:
                grading_breakdown["Code Quality"] = 30
                total_grade += 30
            else:
                grading_breakdown["Code Quality"] = 15
                total_grade += 15
        else:
            grading_breakdown["Code Quality"] = 0
    except Exception as e:
        grading_breakdown["Code Quality"] = 0

    # 2. Rectangle Coordinates Validation (20 points)
    try:
        # Verify that rectangle coordinates are formatted correctly
        if len(rectangle_coords.strip()) > 0:
            rectangles = rectangle_coords.split("\n")
            valid_rectangles = all(len(rect.split(",")) == 4 for rect in rectangles)
            if valid_rectangles:
                grading_breakdown["Rectangle Coordinates"] = 20
                total_grade += 20
            else:
                grading_breakdown["Rectangle Coordinates"] = 10
                total_grade += 10
        else:
            grading_breakdown["Rectangle Coordinates"] = 0
    except Exception as e:
        grading_breakdown["Rectangle Coordinates"] = 0

    # 3. Thresholded Image Validation (25 points)
    try:
        if os.path.exists(threshold_image_path):
            # Basic check for image validity (you could implement more complex checks here)
            grading_breakdown["Thresholded Image"] = 25
            total_grade += 25
        else:
            grading_breakdown["Thresholded Image"] = 0
    except Exception as e:
        grading_breakdown["Thresholded Image"] = 0

    # 4. Image with Rectangles Validation (25 points)
    try:
        if os.path.exists(rectangle_image_path):
            # Basic check for image validity
            grading_breakdown["Outlined Image"] = 25
            total_grade += 25
        else:
            grading_breakdown["Outlined Image"] = 0
    except Exception as e:
        grading_breakdown["Outlined Image"] = 0

    return total_grade, grading_breakdown

