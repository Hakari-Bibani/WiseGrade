import pandas as pd
import re
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import os


def grade_assignment(code, uploaded_html, uploaded_png, uploaded_csv):
    """
    Grade Assignment 2 based on the provided files and criteria.
    """

    # Define the directory where the correct reference files are located
    base_dir = os.path.dirname(__file__)
    correct_csv_values = {
        "Total Earthquakes": 210.0,
        "Average Magnitude": 4.64,
        "Maximum Magnitude": 7.1,
        "Minimum Magnitude": 4.1,
        "4.0-4.5": 109.0,
        "4.5-5.0": 76.0,
        ">5.0": 25.0,
    }

    grade = 0

    # 1. Library Imports (10 Points)
    required_imports = ["folium", "matplotlib", "seaborn", "requests", "urllib", "pandas"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    grade += min(10, imported_libraries * 2)

    # 2. Code Quality (20 Points)
    code_quality_deductions = 0
    if any(re.match(r"\s*[a-z]\s*=", line) for line in code.split("\n")):
        code_quality_deductions += 1  # Deduct for single-letter variables
    if "=" in code.replace(" = ", ""):
        code_quality_deductions += 1  # Deduct for missing spacing
    if "#" not in code:
        code_quality_deductions += 1  # Deduct for missing comments
    if "\n\n" not in code:
        code_quality_deductions += 1  # Deduct for poor organization
    grade += max(0, 20 - code_quality_deductions * 5)

    # 3. Fetching Data from API (10 Points)
    if "https://earthquake.usgs.gov/fdsnws/event/1/query" in code:
        grade += 3  # Correct API URL
    if "requests.get" in code or "urllib.request" in code:
        grade += 3  # Correct API call
    if "response.status_code" in code:
        grade += 4  # Proper error handling

    # 4. Filtering Earthquakes (10 Points)
    if "magnitude > 4.0" in code:
        grade += 5  # Correct filtering logic
    if all(field in code for field in ["latitude", "longitude", "magnitude", "time"]):
        grade += 5  # Proper data extraction

    # 5. Map Visualization (20 Points)
    try:
        with open(uploaded_html, "r") as html_file:
            uploaded_map = BeautifulSoup(html_file, "html.parser")

        # Check for markers with correct colors
        green_markers = len(uploaded_map.find_all("marker", {"class": "green"}))
        yellow_markers = len(uploaded_map.find_all("marker", {"class": "yellow"}))
        red_markers = len(uploaded_map.find_all("marker", {"class": "red"}))
        total_markers = green_markers + yellow_markers + red_markers

        # Check popups
        popups = uploaded_map.find_all("popup")
        if total_markers > 0 and len(popups) >= total_markers:
            grade += 20
    except Exception as e:
        print(f"Error checking HTML file: {e}")

    # 6. Bar Chart (15 Points)
    try:
        if uploaded_png:
            grade += 12  # Assign 12 points if PNG is uploaded
    except Exception as e:
        print(f"Error checking PNG file: {e}")

    # 7. Text Summary (15 Points)
    try:
        uploaded_summary = pd.read_csv(uploaded_csv)

        # Check for matching values
        matches = 0
        for key, correct_value in correct_csv_values.items():
            if key in uploaded_summary.columns:
                uploaded_value = uploaded_summary[key].iloc[0]
                if abs(uploaded_value - correct_value) < 0.1:  # Allow small tolerance
                    matches += 1

        if matches == len(correct_csv_values):
            grade += 15
    except Exception as e:
        print(f"Error checking CSV file: {e}")

    return round(grade)


# For testing purposes
if __name__ == "__main__":
    try:
        # Test file paths
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

        # Grade the assignment
        score = grade_assignment(student_code, uploaded_html, uploaded_png, uploaded_csv)
        print(f"Student's Grade: {score}/100")
    except Exception as e:
        print(f"Error: {e}")
