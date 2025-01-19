def grade_assignment(code_input, rectangle_grade, thresholded_image_grade, outlined_image_grade):
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
    grading_breakdown["Thresholded Image"] = thresholded_image_grade
    total_grade += thresholded_image_grade
    
    # 5. Image with Rectangles Outlined (4 Points)
    grading_breakdown["Image with Rectangles Outlined"] = outlined_image_grade
    total_grade += outlined_image_grade
    
    return total_grade, grading_breakdown
