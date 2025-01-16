import pandas as pd
import re
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
from difflib import SequenceMatcher
import pytesseract


def grade_assignment(code, uploaded_html, uploaded_png, uploaded_csv):
    """
    Grade Assignment 2 by evaluating the student's code and uploaded files.
    """
    grade = 0

    # **Grading the Script**

    # 1. Library Imports (10 Points)
    required_imports = ["folium", "matplotlib", "requests", "pandas"]
    library_score = 10
    used_libraries = re.findall(r"import\s+(\w+)", code)
    for lib in required_imports:
        if lib not in used_libraries:
            library_score -= 2  # Deduct 2 points for missing library

    unused_libraries = [lib for lib in used_libraries if lib not in required_imports]
    library_score -= len(unused_libraries)  # Deduct 1 point per unused library
    grade += max(0, library_score)

    # 2. Code Quality (20 Points)
    # Variable Naming (5 Points)
    variable_score = 5
    if any(re.match(r"\s*[a-z]\s*=", line) for line in code.split("\n")):
        variable_score -= 1  # Deduct for single-letter variables
    if any(len(var) < 3 for var in re.findall(r"\b\w+\b", code)):
        variable_score -= 1  # Deduct for non-descriptive variable names

    # Spacing (5 Points)
    spacing_score = 5
    if "=" in code.replace(" = ", ""):
        spacing_score -= 1  # Deduct for missing spaces around `=`
    if ">" in code.replace(" > ", "") or "<" in code.replace(" < ", ""):
        spacing_score -= 1  # Deduct for missing spaces around `>` or `<`

    # Comments (5 Points)
    comment_score = 5
    if "#" not in code:
        comment_score -= 2  # Deduct for missing comments
    if code.count("#") > 15:
        comment_score -= 1  # Deduct for over-commenting

    # Organization (5 Points)
    organization_score = 5
    if "\n\n" not in code:
        organization_score -= 1  # Deduct for no blank lines between sections

    grade += variable_score + spacing_score + comment_score + organization_score

    # 3. Fetching Data from the API (10 Points)
    if "https://earthquake.usgs.gov/fdsnws/event/1/query" in code:
        grade += 3  # Correct API URL
    if "requests.get" in code:
        grade += 3  # Successful API call
    if "response.status_code" in code:
        grade += 4  # Proper error handling

    # 4. Filtering Earthquakes (10 Points)
    if "magnitude > 4.0" in code:
        grade += 5  # Correct filtering logic
    if all(field in code for field in ["latitude", "longitude", "magnitude", "time"]):
        grade += 5  # Proper data extraction

    # **Grading Uploaded Files**

    # 5. Map Visualization (20 Points)
    try:
        with open(uploaded_html, "r") as html_file:
            uploaded_soup = BeautifulSoup(html_file, "html.parser")
        with open("correct_map.html", "r") as f:
            correct_soup = BeautifulSoup(f, "html.parser")

        # Extract markers
        uploaded_markers = uploaded_soup.find_all("circlemarker")
        correct_markers = correct_soup.find_all("circlemarker")

        if len(uploaded_markers) != len(correct_markers):
            grade += 0  # Deduct all points if marker count doesn't match
        else:
            map_score = 0
            for u_marker, c_marker in zip(uploaded_markers, correct_markers):
                if "fillColor" in u_marker.attrs and "fillColor" in c_marker.attrs:
                    if u_marker["fillColor"] == c_marker["fillColor"]:
                        map_score += 3  # Award points for matching colors
                if "popup" in u_marker.attrs and "popup" in c_marker.attrs:
                    if u_marker["popup"] == c_marker["popup"]:
                        map_score += 3  # Award points for matching popups

            grade += min(map_score, 20)  # Cap at 20 points
    except Exception as e:
        print(f"Error grading map: {e}")

    # 6. Bar Chart (15 Points)
    try:
        uploaded_image = np.array(Image.open(uploaded_png).convert("L"))
        correct_image = np.array(Image.open("correct_chart.png").convert("L"))

        # Compare structure using SSIM
        similarity_score = ssim(uploaded_image, correct_image)
        bar_chart_score = 0
        if similarity_score > 0.9:
            bar_chart_score += 10
        elif similarity_score > 0.8:
            bar_chart_score += 8
        elif similarity_score > 0.7:
            bar_chart_score += 5

        # OCR Text Similarity
        uploaded_text = pytesseract.image_to_string(uploaded_png)
        correct_text = pytesseract.image_to_string("correct_chart.png")
        text_similarity = SequenceMatcher(None, uploaded_text, correct_text).ratio()
        if text_similarity > 0.9:
            bar_chart_score += 5
        elif text_similarity > 0.8:
            bar_chart_score += 3

        grade += bar_chart_score
    except Exception as e:
        print(f"Error grading bar chart: {e}")

    # 7. Text Summary (15 Points)
    try:
        uploaded_summary = pd.read_csv(uploaded_csv)
        correct_summary = pd.read_csv("correct_summary.csv")

        # Extract numerical values
        uploaded_values = uploaded_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()
        correct_values = correct_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()

        # Compare values with tolerance
        tolerance = 0.01
        points = 0
        for u_val, c_val in zip(uploaded_values, correct_values):
            if abs(u_val - c_val) <= tolerance:
                points += 1  # Award 1 point per matching value

        grade += min(points, 15)  # Cap at 15 points
    except Exception as e:
        print(f"Error grading text summary: {e}")

    return round(grade)


# For testing purposes
if __name__ == "__main__":
    try:
        student_code = """
        import requests
        import pandas as pd
        import folium
        from matplotlib import pyplot as plt
        # Dummy code example
        """
        uploaded_html = "uploaded_map.html"
        uploaded_png = "uploaded_chart.png"
        uploaded_csv = "uploaded_summary.csv"

        score = grade_assignment(student_code, uploaded_html, uploaded_png, uploaded_csv)
        print(f"Student's Grade: {score}/100")
    except Exception as e:
        print(f"Error: {e}")
