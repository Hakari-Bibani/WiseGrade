import pandas as pd
import os
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np

def grade_assignment(code, html_file, bar_chart_file, summary_file):
    grade = 0

    # 1. Library Imports (10 Points)
    required_imports = ["folium", "matplotlib", "requests", "pandas"]
    import_penalty = 0

    # Check for required libraries
    for lib in required_imports:
        if lib not in code:
            import_penalty += 2  # Missing required library
    if "urllib" in code and "requests" not in code:
        import_penalty -= 2  # urllib can be an alternative for requests
    grade += max(0, 10 - import_penalty)

    # 2. Code Quality (20 Points)
    # Check variable naming, spacing, comments, and code organization
    code_issues = 0

    # Variable naming
    if any(var in code for var in ["x", "y", "z"]):
        code_issues += 1
    if "earthquake_map" not in code or "magnitude_counts" not in code:
        code_issues += 1

    # Spacing
    if "=" in code.replace(" = ", ""):
        code_issues += 1
    if ":" in code.replace(": ", ""):
        code_issues += 1

    # Comments
    if code.count("#") < len(code.split("\n")) * 0.1:  # Check for lack of comments
        code_issues += 1

    # Organization
    if "\n\n" not in code:
        code_issues += 1

    grade += max(0, 20 - code_issues * 5)

    # 3. Fetching Data from the API (10 Points)
    if "https://earthquake.usgs.gov/fdsnws/event/1/query" in code:
        grade += 3  # Correct API URL
    if "requests.get" in code or "urllib.request" in code:
        grade += 3  # Successful data retrieval
    if "response.status_code" in code or "try:" in code:
        grade += 4  # Proper error handling

    # 4. Filtering Earthquakes (10 Points)
    if "> 4.0" in code:
        grade += 5  # Correct filtering
    if "latitude" in code and "longitude" in code and "time" in code:
        grade += 5  # Proper extraction of data fields

    # 5. Map Visualization (20 Points)
    try:
        with open(html_file, "r") as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, "html.parser")
            markers = soup.find_all("marker")
            if markers:
                grade += 10  # Map contains markers
            # Check for color coding
            for marker in markers:
                if "green" in str(marker):
                    grade += 5
                elif "yellow" in str(marker):
                    grade += 5
                elif "red" in str(marker):
                    grade += 5
    except Exception as e:
        print(f"Error processing HTML file: {e}")

    # 6. Bar Chart (15 Points)
    try:
        correct_chart = cv2.imread("correct_bar_chart.png", cv2.IMREAD_GRAYSCALE)
        submitted_chart = cv2.imread(bar_chart_file, cv2.IMREAD_GRAYSCALE)
        if correct_chart is not None and submitted_chart is not None:
            similarity, _ = ssim(correct_chart, submitted_chart, full=True)
            if similarity > 0.9:  # Similarity threshold
                grade += 15
            else:
                grade += int(similarity * 15)
    except Exception as e:
        print(f"Error processing bar chart: {e}")

    # 7. Text Summary (15 Points)
    try:
        summary = pd.read_csv(summary_file)
        expected_data = {
            "Total": 25,  # Replace with correct expected values
            "Average": 4.5,
            "Maximum": 6.0,
            "Minimum": 4.1,
            "Range 4.0-4.5": 10,
            "Range 4.5-5.0": 8,
            "Range > 5.0": 7,
        }

        score_per_field = 15 / len(expected_data)
        for key, expected_value in expected_data.items():
            if key in summary.columns and round(summary[key].iloc[0], 1) == expected_value:
                grade += score_per_field
    except Exception as e:
        print(f"Error processing CSV summary: {e}")

    return round(grade)

# Example usage:
# grade = grade_assignment(code_string, "submission_map.html", "bar_chart.png", "summary.csv")
# print(f"Final Grade: {grade}/100")
