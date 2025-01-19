import cv2
import numpy as np
import os
from PIL import Image

def grade_assignment(code_input, thresholded_image_path, outlined_image_path):
    grade = 0
    grading_breakdown = {}
def grade_assignment(code_input, thresh_image_path, outlined_image_path):
    """
    Grades the Assignment 4 submission.
    # Step 1: Check Library Imports (15 Points)
    grading_breakdown['Library Imports'] = 0
    required_libraries = ['cv2', 'numpy', 'matplotlib']
    for lib in required_libraries:
        if lib in code_input:
            grade += 5
            grading_breakdown['Library Imports'] += 5
    Args:
        code_input (str): The code submitted by the student.
        thresh_image_path (str): Path to the uploaded thresholded image.
        outlined_image_path (str): Path to the uploaded outlined image.
    # Step 2: Code Quality (20 Points)
    grading_breakdown['Code Quality'] = 0
    if all(var in code_input for var in ['variable_name', 'descriptive_name']):  # Example variable naming check
        grade += 5
        grading_breakdown['Code Quality'] += 5
    if ' ' in code_input and '    ' in code_input:  # Example spacing check
        grade += 5
        grading_breakdown['Code Quality'] += 5
    if '#' in code_input:  # Example comment check
        grade += 5
        grading_breakdown['Code Quality'] += 5
    if 'def ' in code_input and '\n\n' in code_input:  # Example organization check
        grade += 5
        grading_breakdown['Code Quality'] += 5
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

    # Step 3: Detected Rectangle Coordinates (28 Points)
    grading_breakdown['Rectangle Coordinates'] = 0
    correct_rectangles = [
        ((1655, 1305), (2021, 1512)),  # Example for Rectangle 1
        # Add all other rectangle coordinates...
    ]
    # Step 1: Evaluate the Code
    try:
        img = cv2.imread(outlined_image_path, cv2.IMREAD_COLOR)
        detected_rectangles = detect_rectangles(img)  # Function to detect rectangles
        for i, rect in enumerate(correct_rectangles):
            if i < len(detected_rectangles) and detected_rectangles[i] == rect:
                grade += 2
                grading_breakdown['Rectangle Coordinates'] += 2
        # Example: Check if the code contains required functions or libraries
        if "cv2" in code_input or "PIL" in code_input:
            grading_breakdown["Code Quality"] = 30  # Assign full marks for code containing required libraries
        else:
            grading_breakdown["Code Quality"] = 15  # Partial marks if libraries are missing
        total_grade += grading_breakdown["Code Quality"]
    except Exception as e:
        grading_breakdown['Rectangle Coordinates Error'] = str(e)
        print(f"Error grading code: {e}")

    # Step 4: Thresholded Image (20 Points)
    grading_breakdown['Thresholded Image'] = 0
    # Step 2: Validate Threshold Image
    try:
        img_thresh = cv2.imread(thresholded_image_path, cv2.IMREAD_GRAYSCALE)
        num_detected_rectangles = len(detect_rectangles(img_thresh))
        correct_num_rectangles = 14  # Example correct number of rectangles
        if num_detected_rectangles == correct_num_rectangles:
            grade += 20
            grading_breakdown['Thresholded Image'] += 20
        if os.path.exists(thresh_image_path):
            thresh_image = Image.open(thresh_image_path)
            # Example: Check if the image is grayscale
            if thresh_image.mode == "L":
                grading_breakdown["Threshold Image Validation"] = 30
            else:
                grading_breakdown["Threshold Image Validation"] = 15
            total_grade += grading_breakdown["Threshold Image Validation"]
    except Exception as e:
        grading_breakdown['Thresholded Image Error'] = str(e)
        print(f"Error validating threshold image: {e}")

    # Step 5: Rectangles Outlined Image (17 Points)
    grading_breakdown['Outlined Image'] = 0
    # Step 3: Validate Outlined Image
    try:
        img_outlined = cv2.imread(outlined_image_path, cv2.IMREAD_COLOR)
        outlined_detected = len(detect_rectangles(img_outlined)) == len(correct_rectangles)
        if outlined_detected:
            grade += 17
            grading_breakdown['Outlined Image'] += 17
    except Exception as e:
        grading_breakdown['Outlined Image Error'] = str(e)
        if os.path.exists(outlined_image_path):
            outlined_image = Image.open(outlined_image_path)

    return grade, grading_breakdown
            # Example: Check if the image contains rectangles (placeholder logic)
            # In real-world scenarios, use a library like OpenCV for rectangle detection.
            if "Rectangle Detected" in outlined_image.info.get("description", ""):  # Placeholder logic
                grading_breakdown["Outlined Image Validation"] = 40
            else:
                grading_breakdown["Outlined Image Validation"] = 20

            total_grade += grading_breakdown["Outlined Image Validation"]
    except Exception as e:
        print(f"Error validating outlined image: {e}")

def detect_rectangles(image):
    # Dummy function for rectangle detection
    return []  # Replace with actual detection logic
    # Return total grade and breakdown
    return total_grade, grading_breakdown
