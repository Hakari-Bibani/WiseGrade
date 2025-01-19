import cv2
import numpy as np

def grade_assignment(code, thresh_image_path, outlined_image_path):
    total_score = 100
    grading_breakdown = {}

    # 1. Library Imports (15 Points)
    required_libraries = {
        "cv2": 5,
        "numpy": 5,
        "matplotlib.pyplot": 5,
    }
    import_points = 0
    for lib, points in required_libraries.items():
        if lib in code:
            import_points += points
    grading_breakdown["Library Imports"] = import_points
    total_score -= (15 - import_points)

    # 2. Code Quality (20 Points)
    code_quality_points = 20
    if " " not in code and "\t" not in code:
        code_quality_points -= 5  # Deduct for spacing issues
    if "#" not in code:
        code_quality_points -= 5  # Deduct for missing comments
    grading_breakdown["Code Quality"] = code_quality_points
    total_score -= (20 - code_quality_points)

    # 3. Rectangle Coordinates (28 Points)
    correct_coordinates = [
        {"top_left": (1655, 1305), "bottom_right": (2021, 1512)},
        {"top_left": (459, 1305), "bottom_right": (825, 1512)},
        # ... (Add the rest here)
    ]
    try:
        # Simulate rectangle detection logic (replace with actual implementation)
        detected_rectangles = [
            # Load coordinates from the output of the student's code
        ]
        rect_points = 28
        for i, correct_rect in enumerate(correct_coordinates):
            if i < len(detected_rectangles):
                if (
                    detected_rectangles[i]["top_left"] == correct_rect["top_left"]
                    and detected_rectangles[i]["bottom_right"] == correct_rect["bottom_right"]
                ):
                    continue  # Rectangle matches
                else:
                    rect_points -= 2  # Deduct 2 points per incorrect rectangle
        grading_breakdown["Rectangle Coordinates"] = rect_points
        total_score -= (28 - rect_points)
    except Exception:
        grading_breakdown["Rectangle Coordinates"] = 0
        total_score -= 28  # Deduct full marks for failure

    # 4. Thresholded Image (20 Points)
    try:
        thresh_image = cv2.imread(thresh_image_path, 0)
        contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected_rect_count = len(contours)
        correct_rect_count = 14  # Assuming the correct thresholded image detects 14 rectangles
        thresh_points = 20 if detected_rect_count == correct_rect_count else max(0, 20 - abs(detected_rect_count - correct_rect_count))
        grading_breakdown["Thresholded Image"] = thresh_points
        total_score -= (20 - thresh_points)
    except Exception:
        grading_breakdown["Thresholded Image"] = 0
        total_score -= 20

    # 5. Outlined Rectangles (17 Points)
    try:
        outlined_image = cv2.imread(outlined_image_path)
        # Simulate outlined rectangle detection (replace with actual implementation)
        outlined_rectangles_detected = True  # Placeholder condition
        outline_points = 17 if outlined_rectangles_detected else 0
        grading_breakdown["Outlined Rectangles"] = outline_points
        total_score -= (17 - outline_points)
    except Exception:
        grading_breakdown["Outlined Rectangles"] = 0
        total_score -= 17

    return total_score, grading_breakdown

