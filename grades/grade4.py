import cv2

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
        correct_rectangles = 14
        outlined_rectangles = count_rectangles_in_image(outlined_image_path)
        grading_breakdown["Image with Rectangles Outlined"] = 4 if outlined_rectangles == correct_rectangles else 0
        total_grade += grading_breakdown["Image with Rectangles Outlined"]
    except Exception as e:
        grading_breakdown["Image with Rectangles Outlined"] = 0
        print(f"Error processing outlined image: {e}")

    return total_grade, grading_breakdown

# Helper function to count rectangles in the image
def count_rectangles_in_image(image_path):
    """
    Counts the number of rectangles detected in the image.
    """
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return len(contours)
    except Exception as e:
        print(f"Error in count_rectangles_in_image: {e}")
        return 0
