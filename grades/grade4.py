def grade_thresholded_image(uploaded_image_path):
    """
    Enhanced grading for thresholded image with better rectangle detection
    """
    import cv2
    import numpy as np
    
    try:
        # Read image
        image = cv2.imread(uploaded_image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return 0, "Failed to read image. Make sure it's a valid image file."
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        
        # Try multiple threshold methods
        _, binary1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        _, binary2 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        adaptive = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Try finding contours in all binary versions
        methods = [binary1, binary2, adaptive]
        best_count = 0
        
        for binary in methods:
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            valid_rectangles = 0
            
            for contour in contours:
                # Multiple approaches to validate rectangles
                # 1. By area
                area = cv2.contourArea(contour)
                if area < 100:  # Skip very small contours
                    continue
                    
                # 2. By shape approximation
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                
                # 3. By aspect ratio
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w)/h
                
                # Accept if either the shape is approximately rectangular
                # or the aspect ratio and area suggest a rectangle
                if (len(approx) == 4 or (0.5 <= aspect_ratio <= 2.0)):
                    valid_rectangles += 1
            
            best_count = max(best_count, valid_rectangles)
        
        # Grade based on best count
        if best_count >= 14:
            return 20, f"Detected {best_count} rectangles: Full 20 points"
        elif best_count > 7:
            points = int(20 * (best_count / 14))
            return points, f"Detected {best_count} rectangles: {points} points"
        else:
            return 0, f"Only detected {best_count} rectangles: 0 points. Try adjusting your thresholding."
            
    except Exception as e:
        return 0, f"Error: {str(e)}. Try re-saving your image as PNG."

def grade_outlined_image(uploaded_path, correct_path="grades/correct_files/correct_outlined.png"):
    """
    Enhanced grading for outlined image with more flexible comparison
    """
    import cv2
    import numpy as np
    
    try:
        # Read images
        uploaded = cv2.imread(uploaded_path)
        correct = cv2.imread(correct_path)
        
        if uploaded is None:
            return 0, "Failed to read uploaded image. Try saving as PNG."
        if correct is None:
            return 0, "Reference image not found. Contact instructor."
            
        # Resize uploaded image if dimensions don't match
        if uploaded.shape != correct.shape:
            uploaded = cv2.resize(uploaded, (correct.shape[1], correct.shape[0]))
            
        # Convert both to grayscale for more flexible comparison
        uploaded_gray = cv2.cvtColor(uploaded, cv2.COLOR_BGR2GRAY)
        correct_gray = cv2.cvtColor(correct, cv2.COLOR_BGR2GRAY)
        
        # Calculate structural similarity index
        from skimage.metrics import structural_similarity as ssim
        similarity = ssim(uploaded_gray, correct_gray)
        
        # More lenient grading based on similarity
        if similarity > 0.8:
            return 4, "Image matches reference well: 4 points"
        elif similarity > 0.6:
            return 2, f"Partial match (similarity: {similarity:.2f}): 2 points"
        else:
            return 0, f"Low similarity ({similarity:.2f}). Check rectangle positions and lines."
            
    except Exception as e:
        return 0, f"Error: {str(e)}. Try re-saving your image as PNG."
