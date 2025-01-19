def grade_assignment(code_input, rectangle_grade, thresholded_image_grade, outlined_image_grade):
    total_grade = 0
    grading_breakdown = {}

    # 1. Library Imports (20 Points)
    libraries = {
        "cv2": 4, "Pillow": 4, "scikit-image": 4, "ImageAI": 4,
        "numpy": 3, "SciPy": 3, "TensorFlow": 3, "PyTorch": 3,
        "matplotlib": 3, "plotly": 3, "seaborn": 3
    }
    library_score = 0
    for lib, points in libraries.items():
        if lib in code_input:
            library_score += points
    grading_breakdown["Library Imports"] = min(library_score, 20)
    total_grade += grading_breakdown["Library Imports"]

    # 2. Code Quality (14 Points)
    code_quality = {
        "Variable Naming": 4 if "x" not in code_input or "y" not in code_input else 0,
        "Spacing": 2 if " =" not in code_input and "= " not in code_input else 0,
        "Comments": 2 if "#" in code_input else 0,
        "Code Organization": 2 if "\n\n" in code_input else 0,
    }
    grading_breakdown["Code Quality"] = sum(code_quality.values())
    total_grade += grading_breakdown["Code Quality"]

    # 3. Rectangle Coordinates (56 Points)
    grading_breakdown["Rectangle Coordinates"] = rectangle_grade
    total_grade += rectangle_grade

    # 4. Thresholded Image (5 Points)
    grading_breakdown["Thresholded Image"] = thresholded_image_grade
    total_grade += thresholded_image_grade

    # 5. Image with Rectangles Outlined (5 Points)
    grading_breakdown["Image with Rectangles Outlined"] = outlined_image_grade
    total_grade += outlined_image_grade

    return total_grade, grading_breakdown
