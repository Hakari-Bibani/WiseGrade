import cv2
import numpy as np

def grade_assignment(code, rectangle_coords, threshold_image_path, outlined_image_path):
    total_grade = 0
    grading_breakdown = {}

    # 1. Library Imports (15 Points)
    grading_breakdown["Library Imports"] = 0
    libraries = ["cv2", "numpy", "matplotlib", "PIL", "scipy", "tensorflow", "torch", "seaborn", "plotly"]
    for lib in libraries:
        if f"import {lib}" in code or f"from {lib}" in code:
            grading_breakdown["Library Imports"] += 5
            if grading_breakdown["Library Imports"] >= 15:
                break

    total_grade += grading_breakdown["Library Imports"]

    # 2. Code Quality (20 Points)
    grading_breakdown["Code Quality"] = 20
    # Deduct for non-descriptive variable names (example: "x", "y")
    if any(var in code for var in [" x ", " y ", " z "]):
        grading_breakdown["Code Quality"] -= 5
    # Deduct for improper spacing (e.g., "a=10" instead of "a = 10")
    if "=" in code and " = " not in code:
        grading_breakdown["Code Quality"] -= 5
    # Deduct for missing comments
    if "#" not in code:
        grading_breakdown["Code Quality"] -= 5
    # Deduct for poor code organization
    if "\n\n" not in code:
        grading_breakdown["Code Quality"] -= 5

    total_grade += grading_breakdown["Code Quality"]

    # 3. Detected Rectangle Coordinates (28 Points)
    grading_breakdown["Rectangle Coordinates"] = 0
    correct_coords = {
        1: ((1655, 1305), (2021, 1512)),
        2: ((459, 1305), (825, 1512)),
        3: ((2051, 1305), (2417, 1512)),
        4: ((1257, 1305), (1623, 1512)),
        5: ((857, 1305), (1223, 1512)),
        6: ((63, 1305), (429, 1512)),
        7: ((157, 1050), (398, 1122)),
        8: ((351, 869), (592, 941)),
        9: ((624, 744), (865, 816)),
        10: ((888, 646), (1129, 718)),
        11: ((1069, 492), (1311, 564)),
        12: ((1338, 360), (1579, 432)),
        13: ((64, 231), (800, 506)),
        14: ((2103, 166), (2344, 239))
    }

    student_coords = rectangle_coords.split("\n")
    for i, rect in enumerate(correct_coords.values(), start=1):
        try:
            student_rect = tuple(map(int, student_coords[i - 1].strip("() ").split(",")))
            if student_rect == rect:
                grading_breakdown["Rectangle Coordinates"] += 2
        except Exception:
            continue

    total_grade += grading_breakdown["Rectangle Coordinates"]

    # 4. Thresholded Image Check (20 Points)
    grading_breakdown["Thresholded Image"] = 0
    try:
        correct_threshold_image = cv2.imread("correct_files/correct_thresholded_image.png", 0)
        student_threshold_image = cv2.imread(threshold_image_path, 0)
        if correct_threshold_image.shape == student_threshold_image.shape:
            diff = cv2.absdiff(correct_threshold_image, student_threshold_image)
            non_zero_count = np.count_nonzero(diff)
            if non_zero_count < 1000:  # Allow minor differences
                grading_breakdown["Thresholded Image"] = 20
    except Exception:
        pass

    total_grade += grading_breakdown["Thresholded Image"]

    # 5. Rectangles Outlined Check (17 Points)
    grading_breakdown["Rectangles Outlined"] = 0
    try:
        correct_outlined_image = cv2.imread("correct_files/correct_outlined_image.png")
        student_outlined_image = cv2.imread(outlined_image_path)
        if correct_outlined_image.shape == student_outlined_image.shape:
            diff = cv2.absdiff(correct_outlined_image, student_outlined_image)
            non_zero_count = np.count_nonzero(diff)
            if non_zero_count < 2000:  # Allow minor differences
                grading_breakdown["Rectangles Outlined"] = 17
    except Exception:
        pass

    total_grade += grading_breakdown["Rectangles Outlined"]

    return total_grade, grading_breakdown
