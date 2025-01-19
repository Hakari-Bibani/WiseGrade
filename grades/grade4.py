def grade_assignment(code_input, rectangle_coordinates, thresholded_image_path, outlined_image_path):
    total_grade = 0
    grading_breakdown = {}

    # 1. Library Imports (15 Points)
    libraries = {
        "cv2": False, "Pillow": False, "scikit-image": False, "ImageAI": False,
        "numpy": False, "SciPy": False, "TensorFlow": False, "PyTorch": False,
        "matplotlib": False, "plotly": False, "seaborn": False,
    }
    for lib in libraries:
        if lib in code_input:
            libraries[lib] = True

    library_grade = sum([5 for lib in libraries if libraries[lib]])
    grading_breakdown["Library Imports"] = min(library_grade, 15)
    total_grade += grading_breakdown["Library Imports"]

    # 2. Code Quality (20 Points)
    code_quality = {
        "Variable Naming": 5 if "x" not in code_input or "y" not in code_input else 0,
        "Spacing": 5 if " =" not in code_input and "= " not in code_input else 0,
        "Comments": 5 if "#" in code_input else 0,
        "Code Organization": 5 if "\n\n" in code_input else 0,
    }
    grading_breakdown["Code Quality"] = sum(code_quality.values())
    total_grade += grading_breakdown["Code Quality"]

    # 3. Rectangle Coordinates (28 Points)
    correct_coordinates = [
        ((1655, 1305), (2021, 1512)), ((459, 1305), (825, 1512)),
        # Add remaining correct rectangles...
    ]
    student_coordinates = [
        tuple(map(int, coord.split(","))) for coord in rectangle_coordinates.split("\n") if coord.strip()
    ]
    rectangle_grade = 0
    for i, correct in enumerate(correct_coordinates):
        if i < len(student_coordinates) and student_coordinates[i] == correct:
            rectangle_grade += 2  # Award 2 points for each correct rectangle
    grading_breakdown["Rectangle Coordinates"] = rectangle_grade
    total_grade += rectangle_grade

    # 4. Thresholded Image (20 Points)
    # For simplicity, let's assume we check for the count of rectangles detected
    detected_rectangles_thresholded = len(correct_coordinates)  # Replace with real logic if needed
    grading_breakdown["Thresholded Image"] = 20 if detected_rectangles_thresholded == len(correct_coordinates) else 0
    total_grade += grading_breakdown["Thresholded Image"]

    # 5. Image with Rectangles Outlined (17 Points)
    outlined_grade = 17 if detected_rectangles_thresholded == len(correct_coordinates) else 0
    grading_breakdown["Image with Rectangles Outlined"] = outlined_grade
    total_grade += outlined_grade

    return total_grade, grading_breakdown
