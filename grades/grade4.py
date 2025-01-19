import cv2
import numpy as np

def grade_assignment(code_input, thresh_image_path, outlined_image_path):
    grade = 0
    breakdown = {}

    # 1. Library Imports (15 Points)
    libraries = ["cv2", "numpy", "matplotlib"]
    imported_libraries = [lib for lib in libraries if lib in code_input]
    grade += len(imported_libraries) * 5
    breakdown["Library Imports"] = len(imported_libraries) * 5

    # 2. Code Quality (20 Points)
    if " " in code_input: grade += 5  # Simple check for spacing
    if "#" in code_input: grade += 5  # Simple check for comments
    if "\n\n" in code_input: grade += 5  # Check for logical blocks
    breakdown["Code Quality"] = grade - sum(breakdown.values())

    # 3. Rectangle Detection (28 Points)
    # Validate rectangles
    expected_rectangles = [
        ((1655, 1305), (2021, 1512)),  # Rectangle 1
        # ... Add all other rectangles
    ]
    image = cv2.imread(thresh_image_path, cv2.IMREAD_GRAYSCALE)
    # Implement your rectangle detection logic here...
    # Compare detected rectangles with expected_rectangles
    grade += 28
    breakdown["Rectangle Detection"] = 28

    # 4. Thresholded Image Verification (20 Points)
    # Validate thresholded image content
    grade += 20
    breakdown["Thresholded Image Verification"] = 20

    # 5. Rectangles Outlined Verification (17 Points)
    # Validate outlined image content
    grade += 17
    breakdown["Outlined Rectangles"] = 17

    return grade, breakdown
