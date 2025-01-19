import cv2
import numpy as np
import os

def grade_assignment(code, coordinates_input, threshold_image_path, outlined_image_path):
    total_score = 0
    grading_breakdown = {}

    # 1. Library Imports (15 Points)
    libraries = {
        "OpenCV": "cv2" in code,
        "Pillow": "PIL" in code,
        "Scikit-Image": "skimage" in code or "sklearn" in code,
        "ImageAI": "imageai" in code,
        "NumPy": "numpy" in code,
        "SciPy": "scipy" in code,
        "TensorFlow": "tensorflow" in code,
        "PyTorch": "torch" in code,
        "Matplotlib": "matplotlib" in code,
        "Plotly": "plotly" in code,
        "Seaborn": "seaborn" in code,
    }

    library_score = sum(5 for key, used in libraries.items() if used)
    grading_breakdown["Library Imports"] = min(library_score, 15)
    total_score += grading_breakdown["Library Imports"]

    # 2. Code Quality (20 Points)
    quality_score = 20
    if any(var in code for var in [" x ", " y "]):  # Variable naming
        quality_score -= 5
    if "=" in code and not (" = " in code):  # Spacing
        quality_score -= 5
    if not any(comment in code for comment in ["#", "\"\"\""]):  # Comments
        quality_score -= 5
    if code.count("\n\n") < 3:  # Code organization
        quality_score -= 5

    grading_breakdown["Code Quality"] = quality_score
    total_score += quality_score

    # 3. Rectangle Coordinates (28 Points)
    correct_coordinates = [
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
        ((2103, 166), (2344, 239)),
    ]

    detected_coordinates = [
        tuple(map(int, coord.strip().split(","))) for coord in coordinates_input.splitlines()
    ]
    rectangle_score = 0

    for i, (correct, detected) in enumerate(zip(correct_coordinates, detected_coordinates)):
        if correct == detected:
            rectangle_score += 2

    grading_breakdown["Rectangle Coordinates"] = rectangle_score
    total_score += rectangle_score

    # 4. Thresholded Image (20 Points)
    threshold_image = cv2.imread(threshold_image_path, 0)
    contours, _ = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_count = len(contours)

    if detected_count == 14:  # Correct number of rectangles
        grading_breakdown["Thresholded Image"] = 20
        total_score += 20
    else:
        grading_breakdown["Thresholded Image"] = 0

    # 5. Outlined Image (17 Points)
    outlined_image = cv2.imread(outlined_image_path)
    outlined_gray = cv2.cvtColor(outlined_image, cv2.COLOR_BGR2GRAY)
    _, outlined_contours, _ = cv2.findContours(outlined_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(outlined_contours) == 14:  # All rectangles outlined
        grading_breakdown["Outlined Image"] = 17
        total_score += 17
    else:
        grading_breakdown["Outlined Image"] = 0

    return total_score, grading_breakdown
