import pandas as pd
import re
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import os

def grade_assignment(code, uploaded_html, uploaded_png, uploaded_csv):
    # Define paths for reference files in the same folder as this script
    base_dir = os.path.dirname(__file__)
    correct_html = os.path.join(base_dir, "correct_map.html")
    correct_png = os.path.join(base_dir, "correct_chart.png")
    correct_csv = os.path.join(base_dir, "correct_summary.csv")

    # Verify reference files exist
    if not all(os.path.exists(f) for f in [correct_html, correct_png, correct_csv]):
        raise FileNotFoundError("Reference files (correct_map.html, correct_chart.png, correct_summary.csv) are missing.")

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
    with open(uploaded_html, "r") as html_file:
        uploaded_map = BeautifulSoup(html_file, "html.parser")
    with open(correct_html, "r") as correct_map_file:
        correct_map = BeautifulSoup(correct_map_file, "html.parser")

    # Check for markers in uploaded map
    uploaded_markers = len(uploaded_map.find_all("marker"))
    correct_markers = len(correct_map.find_all("marker"))
    if uploaded_markers >= correct_markers:
        grade += 10

    # Verify marker colors and popup data (add logic as necessary)
    grade += 10  # Placeholder for successful verification

    # 6. Bar Chart (15 Points)
    uploaded_image = np.array(Image.open(uploaded_png).convert("L"))
    correct_image = np.array(Image.open(correct_png).convert("L"))
    similarity_score = ssim(uploaded_image, correct_image)

    if similarity_score > 0.9:  # High similarity
        grade += 15
    elif similarity_score > 0.7:  # Moderate similarity
        grade += 10
    else:
        grade += 5

    # 7. Text Summary (15 Points)
    uploaded_summary = pd.read_csv(uploaded_csv)
    correct_summary = pd.read_csv(correct_csv)

    # Compare earthquake counts
    try:
        if len(uploaded_summary) == len(correct_summary):
            grade += 5

        # Check statistics
        for col in ["Total Earthquakes", "Average Magnitude", "Maximum Magnitude", "Minimum Magnitude"]:
            if abs(uploaded_summary[col][0] - correct_summary[col][0]) < 0.1:  # Small tolerance
                grade += 2.5
    except KeyError:
        pass

    return round(grade)
