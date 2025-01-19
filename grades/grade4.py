import cv2
import numpy as np

def grade_assignment(code, rectangle_coords, threshold_image_path, outlined_image_path):
    total_score = 100
    grading_breakdown = {}

    # 1. Library Imports (15 Points)
    libraries_score = 0
    required_libraries = [
        {"names": ["cv2", "PIL", "skimage", "imageai"], "points": 5},
        {"names": ["numpy", "scipy", "tensorflow", "torch"], "points": 5},
        {"names": ["matplotlib", "plotly", "seaborn", "PIL"], "points": 5},
    ]

    for library_group in required_libraries:
        if any(lib in code for lib in library_group["names"]):
            libraries_score += library_group["points"]

    grading_breakdown["Library Imports"] = libraries_score

    # 2. Code Quality (20 Points)
    code_quality_score = 20

    if not any(len(var.strip()) > 1 for var in ["x", "y"]):
        code_quality_score -= 5  # Deduct for bad variable names

    if "=" in code and "=" not in code.replace(" ", ""):
        code_quality_score -= 5  # Deduct for improper spacing

    if "#" not in code:
        code_quality_score -= 5  # Deduct for no comments

    if not any(block in code for block in ["def ", "class "]):
        code_quality_score -= 5  # Deduct for poor organization

    grading_breakdown["Code Quality"] = code_quality_score

    # 3. Detected Rectangle Coordinates (28 Points)
    correct_coords = [
        ((1655, 1305), (2021, 1512)), ((459, 1305), (825, 1512)),
        ((2051, 1305), (2417, 1512)), ((1257, 1305), (1623, 1512)),
        ((857, 1305), (1223, 1512)), ((63, 1305), (429, 1512)),
        ((157, 1050), (398, 1122)), ((351, 869), (592, 941)),
        ((624, 744), (865, 816)), ((888, 646), (1129, 718)),
        ((1069, 492), (1311, 564)), ((1338, 360), (1579, 432)),
        ((64, 231), (800, 506)), ((2103, 166), (2344, 239))
    ]

    coord_score = 0
    try:
        student_coords = eval(rectangle_coords)  # Assumes input is Python tuple format
        for idx, (top_left, bottom_right) in enumerate(correct_coords):
            if idx < len(student_coords):
                if student_coords[idx] == (top_left, bottom_right):
                    coord_score += 2
    except Exception:
        pass

    grading_breakdown["Detected Rectangle Coordinates"] = coord_score

    # 4. Upload Thresholded Image (20 Points)
    threshold_score = 0
    try:
        threshold_img = cv2.imread(threshold_image_path, 0)
        contours, _ = cv2.findContours(threshold_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected_rectangles = len(contours)

        if detected_rectangles == 14:  # Assuming 14 is the correct number
            threshold_score = 20
        else:
            threshold_score = int((detected_rectangles / 14) * 20)  # Partial score
    except Exception:
        pass

    grading_breakdown["Thresholded Image"] = threshold_score

    # 5. Upload Outlined Image (17 Points)
    outlined_score = 0
    try:
        outlined_img = cv2.imread(outlined_image_path)
        outlined_gray = cv2.cvtColor(outlined_img, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(outlined_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected_rectangles = len(contours)

        if detected_rectangles == 14:  # Assuming 14 is correct
            outlined_score = 17
        else:
            outlined_score = int((detected_rectangles / 14) * 17)  # Partial score
    except Exception:
        pass

    grading_breakdown["Outlined Image"] = outlined_score

    # Calculate Total Score
    total_score = sum(grading_breakdown.values())
    return total_score, grading_breakdown
