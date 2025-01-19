def grade_assignment(code_input, thresh_image_path, rect_image_path):
    try:
        # Example grading logic
        total_grade = 0
        grading_breakdown = {}

        # Check code input (placeholder logic)
        if len(code_input) > 0:
            grading_breakdown["code"] = 40
            total_grade += 40
        else:
            grading_breakdown["code"] = 0

        # Check thresholded image (placeholder logic)
        if thresh_image_path.endswith(".png") or thresh_image_path.endswith(".jpg"):
            grading_breakdown["thresholded_image"] = 30
            total_grade += 30
        else:
            grading_breakdown["thresholded_image"] = 0

        # Check rectangle-outlined image (placeholder logic)
        if rect_image_path.endswith(".png") or rect_image_path.endswith(".jpg"):
            grading_breakdown["rectangles_image"] = 30
            total_grade += 30
        else:
            grading_breakdown["rectangles_image"] = 0

        return total_grade, grading_breakdown
    except Exception as e:
        raise ValueError(f"Error in grading: {e}")
