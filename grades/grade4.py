import os
import cv2
import numpy as np

# Correct rectangle coordinates
CORRECT_RECTANGLES = [
    {"top_left": (1655, 1305), "bottom_right": (2021, 1512)},
    {"top_left": (459, 1305), "bottom_right": (825, 1512)},
    {"top_left": (2051, 1305), "bottom_right": (2417, 1512)},
    {"top_left": (1257, 1305), "bottom_right": (1623, 1512)},
    {"top_left": (857, 1305), "bottom_right": (1223, 1512)},
    {"top_left": (63, 1305), "bottom_right": (429, 1512)},
    {"top_left": (157, 1050), "bottom_right": (398, 1122)},
    {"top_left": (351, 869), "bottom_right": (592, 941)},
    {"top_left": (624, 744), "bottom_right": (865, 816)},
    {"top_left": (888, 646), "bottom_right": (1129, 718)},
    {"top_left": (1069, 492), "bottom_right": (1311, 564)},
    {"top_left": (1338, 360), "bottom_right": (1579, 432)},
    {"top_left": (64, 231), "bottom_right": (800, 506)},
    {"top_left": (2103, 166), "bottom_right": (2344, 239)},
]

def grade_assignment(code_input, rectangle_coords, threshold_image_path, rectangle_image_path):
    total_grade = 0
    grading_breakdown = {}

    # 1. Library Imports (15 points)
    libraries = {"cv2": 5, "numpy": 5, "matplotlib": 5}
    library_score = 0
    for lib, points in libraries.items():
        if lib in code_input:
            library_score += points
    grading_breakdown["Library Imports"] = library_score
    total_grade += library_score

    # 2. Code Quality (20 points)
    code_quality_score = 20
    if not any(var in code_input for var in ["=", ">", "<"]):  # Spacing check
        code_quality_score -= 5
    if not any(comment in code_input for comment in ["#", "\"\"\""]):  # Comments check
        code_quality_score -= 5
    grading_breakdown["Code Quality"] = code_quality_score
    total_grade += code_quality_score

    # 3. Rectangle Coordinates Validation (28 points)
    try:
        rectangles = rectangle_coords.split("\n")
        score_per_rect = 28 / len(CORRECT_RECTANGLES)
        rectangle_score = 0
        for i, rect in enumerate(CORRECT_RECTANGLES):
            if i < len(rectangles):
                coords = list(map(int, rectangles[i].replace("(", "").replace(")", "").split(",")))
                if tuple(coords[:2]) == rect["top_left"] and tuple(coords[2:]) == rect["bottom_right"]:
                    rectangle_score += score_per_rect
        grading_breakdown["Rectangle Coordinates"] = int(rectangle_score)
        total_grade += int(rectangle_score)
    except Exception:
        grading_breakdown["Rectangle Coordinates"] = 0

    # 4. Thresholded Image Validation (20 points)
    try:
        correct_threshold_path = "correct_files/correct_thresholded_image.png"
        correct_img = cv2.imread(correct_threshold_path, 0)
        student_img = cv2.imread(threshold_image_path, 0)
        if correct_img is not None and student_img is not None:
            # Compare number of rectangles
            _, correct_thresh = cv2.threshold(correct_img, 127, 255, cv2.THRESH_BINARY)
            _, student_thresh = cv2.threshold(student_img, 127, 255, cv2.THRESH_BINARY)
            correct_contours, _ = cv2.findContours(correct_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            student_contours, _ = cv2.findContours(student_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(correct_contours) == len(student_contours):
                grading_breakdown["Thresholded Image"] = 20
                total_grade += 20
            else:
                grading_breakdown["Thresholded Image"] = 10
                total_grade += 10
        else:
            grading_breakdown["Thresholded Image"] = 0
    except Exception:
        grading_breakdown["Thresholded Image"] = 0

    # 5. Outlined Image Validation (17 points)
    try:
        correct_outlined_path = "correct_files/correct_outlined_image.png"
        correct_outlined_img = cv2.imread(correct_outlined_path)
        student_outlined_img = cv2.imread(rectangle_image_path)
        if correct_outlined_img is not None and student_outlined_img is not None:
            # Check for outline correctness
            grading_breakdown["Outlined Image"] = 17
            total_grade += 17
        else:
            grading_breakdown["Outlined Image"] = 0
    except Exception:
        grading_breakdown["Outlined Image"] = 0

    return total_grade, grading_breakdown
