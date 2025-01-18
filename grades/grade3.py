def grade_assignment(code, html_path, excel_path):
    """
    Grades Assignment 3 based on the provided code, HTML file, and Excel file.
    Returns a numerical grade (0-100).
    """
    total_score = 0

    # Example grading logic (customize as needed):
    if "folium" in code:
        total_score += 20  # Points for using folium
    if "matplotlib" in code or "seaborn" in code:
        total_score += 20  # Points for using matplotlib/seaborn
    if "requests" in code or "urllib" in code:
        total_score += 20  # Points for using requests/urllib
    if "pandas" in code:
        total_score += 20  # Points for using pandas
    if "reportlab" in code:
        total_score += 20  # Points for using reportlab

    # Validate HTML file (example logic)
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            if "folium.Map" in html_content:
                total_score += 10  # Points for generating a folium map
    except Exception as e:
        print(f"Error reading HTML file: {e}")

    # Validate Excel file (example logic)
    try:
        df = pd.read_excel(excel_path)
        if not df.empty:
            total_score += 10  # Points for providing a valid Excel file
    except Exception as e:
        print(f"Error reading Excel file: {e}")

    # Ensure the total score does not exceed 100
    return min(total_score, 100)
