import cv2
import numpy as np

# Correct rectangle coordinates
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
    ((2103, 166), (2344, 239)),    # Rectangle 14
]

def grade_assignment(code, threshold_path, outlined_path):
    """
    Grades Assignment 4 based on the provided code, thresholded image, and outlined image.
    Returns a numerical grade (0-100) with breakdowns.
    """
    total_score = 0
    grading_breakdown = {}

    #### Part 1: Code Grading (35 Points Total) ####

    # Library Imports (15 Points)
    library_score = 0
    if any(lib in code for lib in ["cv2", "PIL", "skimage", "imageai"]):
        library_score += 5
    if any(lib in code for lib in ["numpy", "scipy", "tensorflow", "torch"]):
        library_score += 5
    if any(lib in code for lib in ["matplotlib", "plotly", "seaborn", "PIL"]):
        library_score += 5
    grading_breakdown["Library Imports"] = library_score
    total_score += library_score

    # Code Quality (20 Points)
    code_quality_score = 0
    descriptive_keywords = ["threshold", "rectangle", "contour", "image"]
    if any(word in code for word in descriptive_keywords):
        code_quality_score += 5
    if " = " in code:
        code_quality_score += 5
    if "#" in code:
        code_quality_score += 5
    if "def " in code:
        code_quality_score += 5
    grading_breakdown["Code Quality"] = code_quality_score
    total_score += code_quality_score

    #### Part 2: Rectangle Coordinates (28 Points) ####
    rectangle_score = 0
    try:
        # Load the outlined image
        outlined_image = cv2.imread(outlined_path)
        gray = cv2.cvtColor(outlined_image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Compare detected rectangles with correct coordinates
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            detected_coords = ((x, y), (x + w, y + h))
            if detected_coords in CORRECT_RECTANGLES:
                rectangle_score += 2  # 2 points per correct rectangle
    except Exception as e:
        print(f"Error processing outlined image: {e}")
    grading_breakdown["Rectangle Coordinates"] = rectangle_score
    total_score += rectangle_score

    #### Part 3: Thresholded Image (20 Points) ####
    threshold_score = 0
    try:
        # Load the thresholded image
        threshold_image = cv2.imread(threshold_path, cv2.IMREAD_GRAYSCALE)
        _, binary = cv2.threshold(threshold_image, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if the number of rectangles is correct
        if len(contours) == 14:
            threshold_score = 20
    except Exception as e:
        print(f"Error processing thresholded image: {e}")
    grading_breakdown["Thresholded Image"] = threshold_score
    total_score += threshold_score

    #### Part 4: Outlined Rectangles (17 Points) ####
    outline_score = 0
    try:
        # Check if rectangles are outlined in the image
        outlined_image = cv2.imread(outlined_path)
        gray = cv2.cvtColor(outlined_image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            outline_score = 17
    except Exception as e:
        print(f"Error processing outlined image: {e}")
    grading_breakdown["Outlined Rectangles"] = outline_score
    total_score += outline_score

    # Ensure the total score does not exceed 100
    total_score = min(total_score, 100)
    return total_score, grading_breakdown
