import os
import cv2
import numpy as np
from PIL import Image

# Correct rectangle coordinates for comparison
CORRECT_RECTANGLES = [
    ((1655, 1305), (2021, 1512)),  # Rectangle 1
    ((459, 1305), (825, 1512)),    # Rectangle 2
    ((2051, 1305), (2417, 1512)),  # Rectangle 3
    ((1257, 1305), (1623, 1512)),  # Rectangle 4
    ((857, 1305), (1223, 1512)),   # Rectangle 5
    ((63, 1305), (429, 1512)),     # Rectangle 6
    ((157, 1050), (398, 1122)),    # Rectangle 7
    ((351, 869), (592, 941)),      # Rectangle 8
    ((624, 744), (865, 816)),      # Rectangle 9
    ((888, 646), (1129, 718)),     # Rectangle 10
    ((1069, 492), (1311, 564)),    # Rectangle 11
    ((1338, 360), (1579, 432)),    # Rectangle 12
    ((64, 231), (800, 506)),       # Rectangle 13
    ((2103, 166), (2344, 239))     # Rectangle 14
]

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

    # 1. Library Imports (15 Points)
    try:
        lib_score = 0
        if "cv2" in code_input or "PIL" in code_input or "skimage" in code_input or "imageai" in code_input:
            lib_score += 5
        if "numpy" in code_input or "scipy" in code_input or "tensorflow" in code_input or "torch" in code_input:
            lib_score += 5
        if "matplotlib" in code_input or "plotly" in code_input or "seaborn" in code_input or "PIL" in code_input:
            lib_score += 5
        grading_breakdown["Library Imports"] = lib_score
        total_grade += lib_score
    except Exception as e:
        grading_breakdown["Library Imports"] = 0

    # 2. Code Quality (20 Points)
    try:
        code_quality_score = 0
        # Variable Naming (5 Points)
        if "x" not in code_input and "y" not in code_input:  # Example check for non-descriptive names
            code_quality_score += 5
        # Spacing (5 Points)
        if "=" in code_input and " = " in code_input:  # Example check for proper spacing
            code_quality_score += 5
        # Comments (5 Points)
        if "#" in code_input:  # Example check for comments
            code_quality_score += 5
        # Code Organization (5 Points)
        if "\n\n" in code_input:  # Example check for logical separation
            code_quality_score += 5
        grading_breakdown["Code Quality"] = code_quality_score
        total_grade += code_quality_score
    except Exception as e:
        grading_breakdown["Code Quality"] = 0

    # 3. Rectangle Coordinates Validation (28 Points)
    try:
        rect_score = 0
        student_rectangles = []
        for line in rectangle_coords.strip().split("\n"):
            coords = list(map(int, line.strip().split(",")))
            student_rectangles.append(((coords[0], coords[1]), (coords[2], coords[3])))

        for correct_rect, student_rect in zip(CORRECT_RECTANGLES, student_rectangles):
            if correct_rect == student_rect:
                rect_score += 2  # 2 points per correct rectangle
        grading_breakdown["Rectangle Coordinates"] = rect_score
        total_grade += rect_score
    except Exception as e:
        grading_breakdown["Rectangle Coordinates"] = 0

    # 4. Thresholded Image Validation (20 Points)
    try:
        if os.path.exists(threshold_image_path):
            # Load the correct and student thresholded images
            correct_threshold = cv2.imread("correct_files/correct_thresholded_image.png", cv2.IMREAD_GRAYSCALE)
            student_threshold = cv2.imread(threshold_image_path, cv2.IMREAD_GRAYSCALE)

            # Compare the number of rectangles detected
            correct_rect_count = len(CORRECT_RECTANGLES)
            student_rect_count = count_rectangles(student_threshold)

            if correct_rect_count == student_rect_count:
                grading_breakdown["Thresholded Image"] = 20
                total_grade += 20
            else:
                grading_breakdown["Thresholded Image"] = 10
                total_grade += 10
        else:
            grading_breakdown["Thresholded Image"] = 0
    except Exception as e:
        grading_breakdown["Thresholded Image"] = 0

    # 5. Outlined Image Validation (17 Points)
    try:
        if os.path.exists(rectangle_image_path):
            # Load the correct and student outlined images
            correct_outlined = cv2.imread("correct_files/correct_outlined_image.png")
            student_outlined = cv2.imread(rectangle_image_path)

            # Compare the number of rectangles outlined
            correct_rect_count = len(CORRECT_RECTANGLES)
            student_rect_count = count_rectangles(student_outlined)

            if correct_rect_count == student_rect_count:
                grading_breakdown["Outlined Image"] = 17
                total_grade += 17
            else:
                grading_breakdown["Outlined Image"] = 8
                total_grade += 8
        else:
            grading_breakdown["Outlined Image"] = 0
    except Exception as e:
        grading_breakdown["Outlined Image"] = 0

    return total_grade, grading_breakdown

def count_rectangles(image):
    """
    Counts the number of rectangles in an image using contour detection.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)
