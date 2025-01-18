def grade_assignment(code, url_link, html_path):
    """
    Grades Assignment 3 based on the provided code, URL link, and HTML file.
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

    # Validate URL link (example logic)
    if url_link and ("http://" in url_link or "https://" in url_link):
        total_score += 10  # Points for providing a valid URL

    # Validate HTML file (example logic)
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            if "folium.Map" in html_content:
                total_score += 10  # Points for generating a folium map
    except Exception as e:
        st.error(f"Error reading HTML file: {e}")

    # Ensure the total score does not exceed 100
    return min(total_score, 100)
