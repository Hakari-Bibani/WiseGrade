# grades/grade4.py
import os
import cv2
import numpy as np
from typing import Tuple, Dict

def check_library_imports(code_input: str) -> Tuple[int, Dict[str, int]]:
    """
    Check for required library imports in the code
    Returns: Points earned and breakdown
    """
    points = 0
    breakdown = {}
    
    # Group 1: Image processing libraries (5 points)
    if any(lib in code_input for lib in ['cv2', 'PIL', 'skimage', 'imageai']):
        points += 5
        breakdown['Image Processing Library'] = 5
    else:
        breakdown['Image Processing Library'] = 0

    # Group 2: Numerical processing libraries (5 points)
    if any(lib in code_input for lib in ['numpy', 'scipy', 'tensorflow', 'torch']):
        points += 5
        breakdown['Numerical Library'] = 5
    else:
        breakdown['Numerical Library'] = 0

    # Group 3: Visualization libraries (5 points)
    if any(lib in code_input for lib in ['matplotlib', 'plotly', 'seaborn', 'PIL']):
        points += 5
        breakdown['Visualization Library'] = 5
    else:
        breakdown['Visualization Library'] = 0
        
    return points, breakdown

def check_code_quality(code_input: str) -> Tuple[int, Dict[str, int]]:
    """
    Evaluate code quality based on naming, spacing, comments, and organization
    """
    points = 0
    breakdown = {}
    
    # Variable naming (5 points)
    poor_names = ['x', 'y', 'a', 'b', 'foo', 'bar']
    has_poor_names = any(f" {name} " in f" {code_input} " for name in poor_names)
    if not has_poor_names:
        points += 5
        breakdown['Variable Naming'] = 5
    else:
        breakdown['Variable Naming'] = 0
    
    # Spacing (5 points)
    poor_spacing = ['=+', '=-', '=*', '=/', '><', '<>', '==+', '==-']
    has_poor_spacing = any(pattern in code_input for pattern in poor_spacing)
    if not has_poor_spacing:
        points += 5
        breakdown['Spacing'] = 5
    else:
        breakdown['Spacing'] = 0
    
    # Comments (5 points)
    if '#' in code_input and code_input.count('#') >= 3:
        points += 5
        breakdown['Comments'] = 5
    else:
        breakdown['Comments'] = 0
    
    # Code organization (5 points)
    if code_input.count('\n\n') >= 2:
        points += 5
        breakdown['Code Organization'] = 5
    else:
        breakdown['Code Organization'] = 0
    
    return points, breakdown

def check_rectangle_coordinates(coords_input: str) -> Tuple[int, Dict[str, bool]]:
    """
    Validate rectangle coordinates against correct answers
    """
    correct_coords = {
        1: ((1655, 1305), (2021, 1512)),
        2: ((459, 1305), (825, 1512)),
        3: ((2051, 1305), (2417, 1512)),
        4: ((1257, 1305), (1623, 1512)),
        5: ((857, 1305), (1223, 1512)),
        6: ((63, 1305), (429, 1512)),
        7: ((157, 1050), (398, 1122)),
        8: ((351, 869), (592, 941)),
        9: ((624, 744), (865, 816)),
        10: ((888, 646), (1129, 718)),
        11: ((1069, 492), (1311, 564)),
        12: ((1338, 360), (1579, 432)),
        13: ((64, 231), (800, 506)),
        14: ((2103, 166), (2344, 239))
    }
    
    points = 0
    results = {}
    
    try:
        # Parse submitted coordinates
        submitted_coords = {}
        for line in coords_input.strip().split('\n'):
            if 'Rectangle' in line and ':' in line:
                rect_num = int(line.split(':')[0].split()[-1])
                coords = line.split(':')[1].strip()
                coords = coords.replace('(', '').replace(')', '')
                parts = coords.split(',')
                if len(parts) >= 4:
                    x1, y1 = int(parts[0]), int(parts[1])
                    x2, y2 = int(parts[2]), int(parts[3])
                    submitted_coords[rect_num] = ((x1, y1), (x2, y2))
        
        # Check each rectangle (2 points each)
        for rect_num, correct_coord in correct_coords.items():
            if rect_num in submitted_coords:
                submitted = submitted_coords[rect_num]
                # Allow for small deviation (±5 pixels)
                is_correct = all(abs(s - c) <= 5 for s, c in 
                               zip(submitted[0] + submitted[1], 
                                   correct_coord[0] + correct_coord[1]))
                if is_correct:
                    points += 2
                results[f'Rectangle_{rect_num}'] = is_correct
            else:
                results[f'Rectangle_{rect_num}'] = False
                
    except Exception as e:
        print(f"Error in coordinate validation: {e}")
        results['Error'] = str(e)
    
    return points, results

def check_thresholded_image(image_path: str, correct_image_path: str) -> Tuple[int, Dict[str, int]]:
    """
    Compare submitted thresholded image with correct image
    """
    points = 0
    breakdown = {}
    
    try:
        # Load images
        submitted_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        correct_img = cv2.imread(correct_image_path, cv2.IMREAD_GRAYSCALE)
        
        if submitted_img is not None and correct_img is not None:
            # Resize if needed
            if submitted_img.shape != correct_img.shape:
                submitted_img = cv2.resize(submitted_img, (correct_img.shape[1], correct_img.shape[0]))
            
            # Count rectangles (using simple contour detection)
            _, submitted_contours, _ = cv2.findContours(submitted_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            _, correct_contours, _ = cv2.findContours(correct_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            submitted_count = len(submitted_contours)
            correct_count = len(correct_contours)
            
            # Award points based on accuracy
            if submitted_count == correct_count:
                points = 20
            elif abs(submitted_count - correct_count) <= 2:
                points = 10
            
            breakdown['Rectangle_Count'] = submitted_count
            breakdown['Expected_Count'] = correct_count
            breakdown['Points'] = points
            
    except Exception as e:
        breakdown['Error'] = str(e)
    
    return points, breakdown

def check_outlined_image(image_path: str, correct_image_path: str) -> Tuple[int, Dict[str, int]]:
    """
    Validate the outlined rectangles image
    """
    points = 0
    breakdown = {}
    
    try:
        # Load images
        submitted_img = cv2.imread(image_path)
        correct_img = cv2.imread(correct_image_path)
        
        if submitted_img is not None and correct_img is not None:
            # Resize if needed
            if submitted_img.shape != correct_img.shape:
                submitted_img = cv2.resize(submitted_img, (correct_img.shape[1], correct_img.shape[0]))
            
            # Convert to grayscale for easier comparison
            submitted_gray = cv2.cvtColor(submitted_img, cv2.COLOR_BGR2GRAY)
            correct_gray = cv2.cvtColor(correct_img, cv2.COLOR_BGR2GRAY)
            
            # Detect edges
            submitted_edges = cv2.Canny(submitted_gray, 50, 150)
            correct_edges = cv2.Canny(correct_gray, 50, 150)
            
            # Compare edge detection results
            matching_pixels = np.sum(submitted_edges == correct_edges)
            total_pixels = submitted_edges.size
            match_percentage = (matching_pixels / total_pixels) * 100
            
            # Award points based on match percentage
            if match_percentage >= 90:
                points = 17
            elif match_percentage >= 75:
                points = 12
            elif match_percentage >= 50:
                points = 8
            
            breakdown['Match_Percentage'] = match_percentage
            breakdown['Points'] = points
            
    except Exception as e:
        breakdown['Error'] = str(e)
    
    return points, breakdown

def grade_assignment(code_input: str, rectangle_coords: str, 
                    threshold_image_path: str, rectangle_image_path: str,
                    correct_threshold_path: str, correct_outline_path: str) -> Tuple[int, Dict]:
    """
    Main grading function that coordinates all checks
    """
    total_points = 0
    grading_breakdown = {}
    
    # 1. Library Imports (15 points)
    lib_points, lib_breakdown = check_library_imports(code_input)
    total_points += lib_points
    grading_breakdown['Library_Imports'] = lib_breakdown
    
    # 2. Code Quality (20 points)
    quality_points, quality_breakdown = check_code_quality(code_input)
    total_points += quality_points
    grading_breakdown['Code_Quality'] = quality_breakdown
    
    # 3. Rectangle Coordinates (28 points)
    coord_points, coord_breakdown = check_rectangle_coordinates(rectangle_coords)
    total_points += coord_points
    grading_breakdown['Rectangle_Coordinates'] = coord_breakdown
    
    # 4. Thresholded Image (20 points)
    thresh_points, thresh_breakdown = check_thresholded_image(
        threshold_image_path, correct_threshold_path)
    total_points += thresh_points
    grading_breakdown['Thresholded_Image'] = thresh_breakdown
    
    # 5. Outlined Image (17 points)
    outline_points, outline_breakdown = check_outlined_image(
        rectangle_image_path, correct_outline_path)
    total_points += outline_points
    grading_breakdown['Outlined_Image'] = outline_breakdown
    
    return total_points, grading_breakdown
