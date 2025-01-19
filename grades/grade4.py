import cv2
import numpy as np

def grade_assignment(code_input, thresholded_image_path, outlined_image_path):
    grade = 0
    grading_breakdown = {}

    # Step 1: Check Library Imports (15 Points)
    grading_breakdown['Library Imports'] = 0
    required_libraries = ['cv2', 'numpy', 'matplotlib']
    for lib in required_libraries:
        if lib in code_input:
            grade += 5
            grading_breakdown['Library Imports'] += 5

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

    # Step 3: Detected Rectangle Coordinates (28 Points)
    grading_breakdown['Rectangle Coordinates'] = 0
    correct_rectangles = [
        ((1655, 1305), (2021, 1512)),  # Example for Rectangle 1
        # Add all other rectangle coordinates...
    ]
    try:
        img = cv2.imread(outlined_image_path, cv2.IMREAD_COLOR)
        detected_rectangles = detect_rectangles(img)  # Function to detect rectangles
        for i, rect in enumerate(correct_rectangles):
            if i < len(detected_rectangles) and detected_rectangles[i] == rect:
                grade += 2
                grading_breakdown['Rectangle Coordinates'] += 2
    except Exception as e:
        grading_breakdown['Rectangle Coordinates Error'] = str(e)

    # Step 4: Thresholded Image (20 Points)
    grading_breakdown['Thresholded Image'] = 0
    try:
        img_thresh = cv2.imread(thresholded_image_path, cv2.IMREAD_GRAYSCALE)
        num_detected_rectangles = len(detect_rectangles(img_thresh))
        correct_num_rectangles = 14  # Example correct number of rectangles
        if num_detected_rectangles == correct_num_rectangles:
            grade += 20
            grading_breakdown['Thresholded Image'] += 20
    except Exception as e:
        grading_breakdown['Thresholded Image Error'] = str(e)

    # Step 5: Rectangles Outlined Image (17 Points)
    grading_breakdown['Outlined Image'] = 0
    try:
        img_outlined = cv2.imread(outlined_image_path, cv2.IMREAD_COLOR)
        outlined_detected = len(detect_rectangles(img_outlined)) == len(correct_rectangles)
        if outlined_detected:
            grade += 17
            grading_breakdown['Outlined Image'] += 17
    except Exception as e:
        grading_breakdown['Outlined Image Error'] = str(e)

    return grade, grading_breakdown


def detect_rectangles(image):
    # Dummy function for rectangle detection
    return []  # Replace with actual detection logic
