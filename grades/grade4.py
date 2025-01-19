import cv2
import numpy as np
import os

# Define correct rectangle coordinates
CORRECT_RECTANGLES = [
    ((1655, 1305), (2021, 1512)),
    ((459, 1305), (825, 1512)),
    ((2051, 1305), (2417, 1512)),
    ((1257, 1305), (1623, 1512)),
    ((857, 1305), (1223, 1512)),
    ((63, 1305), (429, 1512)),
    ((157, 1050), (398, 1122)),
    ((351, 869), (592, 941)),
    ((624, 744), (865, 816)),
    ((888, 646), (1129, 718)),
    ((1069, 492), (1311, 564)),
    ((1338, 360), (1579, 432)),
    ((64, 231), (800, 506)),
    ((2103, 166), (2344, 239))
]

# Grading function
def grade_assignment(code: str, rectangle_coords: str, threshold_image_path: str, outlined_image_path: str):
    total_grade = 0
    grading_breakdown = {}

    # Step 1: Check library imports (15 points)
    libraries = {
        "opencv": ["cv2"],
        "numpy": ["numpy"],
        "visualization": ["matplotlib", "plotly", "seaborn", "PIL"]
    }
    points = 0

    for key, lib_list in libraries.items():
        if any(lib in code for lib in lib_list):
            points += 5

    grading_breakdown["Library Imports"] = points
    total_grade += points

    # Step 2: Check code quality (20 points)
    points = 20
    if "x" in code or "y" in code:
        points -= 5  # Deduct for non-descriptive variable names

    if "=" in code and " = " not in code:
        points -= 5  # Deduct for improper spacing

    if "#" not in code:
        points -= 5  # Deduct for missing comments

    if "\n\n" not in code:
        points -= 5  # Deduct for lack of logical separation

    grading_breakdown["Code Quality"] = points
    total_grade += points

    # Step 3: Check rectangle coordinates (28 points)
    points = 28
    try:
        submitted_rectangles = [
            tuple(map(int, coord.strip().split(',')))
            for coord in rectangle_coords.strip().split("\n")
        ]
        for idx, (submitted, correct) in enumerate(zip(submitted_rectangles, CORRECT_RECTANGLES)):
            if submitted != correct:
                points -= 2  # Deduct 2 points for each incorrect rectangle
    except Exception:
        points = 0  # Deduct all points if format is incorrect

    grading_breakdown["Rectangle Coordinates"] = points
    total_grade += points

    # Step 4: Check thresholded image (20 points)
    points = 20
    try:
        threshold_image = cv2.imread(threshold_image_path, cv2.IMREAD_GRAYSCALE)
        if threshold_image is None:
            points = 0
        else:
            contours, _ = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) != len(CORRECT_RECTANGLES):
                points -= 10  # Deduct 10 points if rectangle count is incorrect
    except Exception:
        points = 0  # Deduct all points for errors

    grading_breakdown["Thresholded Image"] = points
    total_grade += points

    # Step 5: Check outlined image (17 points)
    points = 17
    try:
        outlined_image = cv2.imread(outlined_image_path)
        if outlined_image is None:
            points = 0
        else:
            # Placeholder: Verify outlines visually (in real use, automate verification if possible)
            pass
    except Exception:
        points = 0  # Deduct all points for errors

    grading_breakdown["Outlined Image"] = points
    total_grade += points

    return total_grade, grading_breakdown
