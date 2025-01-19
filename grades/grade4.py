def grade_assignment(code_input, rectangle_grade, thresholded_image_path, outlined_image_path):
    total_grade = 0
    grading_breakdown = {}

    # 1. Library Imports (10 Points)
    libraries = {
        "cv2": False, "Pillow": False, "scikit-image": False, "ImageAI": False,
        "numpy": False, "SciPy": False, "TensorFlow": False, "PyTorch": False,
        "matplotlib": False, "plotly": False, "seaborn": False,
    }
    for lib in libraries:
        if lib in code_input:
            libraries[lib] = True

    library_grade = 0
    library_grade += 4 if any(libraries[lib] for lib in ["cv2", "Pillow", "scikit-image", "ImageAI"]) else 0
    library_grade += 3 if any(libraries[lib] for lib in ["numpy", "SciPy", "TensorFlow", "PyTorch"]) else 0
    library_grade += 3 if any(libraries[lib] for lib in ["matplotlib", "plotly", "seaborn"]) else 0
    grading_breakdown["Library Imports"] = library_grade
    total_grade += library_grade

    # 2. Code Quality (10 Points)
    code_quality = {
        "Variable Naming": 4 if "x" not in code_input and "y" not in code_input else 0,
        "Spacing": 2 if " =" not in code_input and "= " not in code_input else 0,
        "Comments": 2 if "#" in code_input else 0,
        "Code Organization": 2 if "\n\n" in code_input else 0,
    }
    grading_breakdown["Code Quality"] = sum(code_quality.values())
    total_grade += grading_breakdown["Code Quality"]

    # 3. Rectangle Coordinates (56 Points)
    grading_breakdown["Rectangle Coordinates"] = rectangle_grade
    total_grade += rectangle_grade

    # 4. Thresholded Image (20 Points)
    try:
        detected_rectangles = count_rectangles_in_image(thresholded_image_path)
        if detected_rectangles >= 14:
            grading_breakdown["Thresholded Image"] = 20
        elif 7 < detected_rectangles < 14:
            grading_breakdown["Thresholded Image"] = int(20 * (detected_rectangles / 14))
        else:
            grading_breakdown["Thresholded Image"] = 0
        total_grade += grading_breakdown["Thresholded Image"]
    except Exception as e:
        grading_breakdown["Thresholded Image"] = 0
        print(f"Error processing thresholded image: {e}")

    # 5. Image with Rectangles Outlined (4 Points)
    try:
        rectangles_outlined_correctly = validate_outlined_image(outlined_image_path)
        grading_breakdown["Image with Rectangles Outlined"] = 4 if rectangles_outlined_correctly else 0
        total_grade += grading_breakdown["Image with Rectangles Outlined"]
    except Exception as e:
        grading_breakdown["Image with Rectangles Outlined"] = 0
        print(f"Error processing outlined image: {e}")

    return total_grade, grading_breakdown

# Helper function to count rectangles in the thresholded image
def count_rectangles_in_image(image_path):
    import cv2
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)

# Helper function to validate outlined rectangles in the image
def validate_outlined_image(image_path):
    import cv2
    correct_values = [
        ((1655, 1305), (2021, 1512)), ((459, 1305), (825, 1512)),
        ((2051, 1305), (2417, 1512)), ((1257, 1305), (1623, 1512)),
        ((857, 1305), (1223, 1512)), ((63, 1305), (429, 1512)),
        ((157, 1050), (398, 1122)), ((351, 869), (592, 941)),
        ((624, 744), (865, 816)), ((888, 646), (1129, 718)),
        ((1069, 492), (1311, 564)), ((1338, 360), (1579, 432)),
        ((64, 231), (800, 506)), ((2103, 166), (2344, 239))
    ]
    image = cv2.imread(image_path)
    detected_rectangles = count_rectangles_in_image(image_path)
    return detected_rectangles == len(correct_values)
