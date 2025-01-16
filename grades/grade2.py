import pandas as pd
import re
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import pytesseract
import os


def grade_assignment(code, uploaded_html, uploaded_png, uploaded_csv):
    """
    Grade Assignment 2 by comparing the student's submission with reference files.
    """

    # Define the directory where the correct reference files are located
    base_dir = os.path.dirname(__file__)
    correct_html = os.path.join(base_dir, "correct_map.html")
    correct_png = os.path.join(base_dir, "correct_chart.png")
    correct_csv = os.path.join(base_dir, "correct_summary.csv")

    # Verify that all reference files exist
    missing_files = [file for file in [correct_html, correct_png, correct_csv] if not os.path.exists(file)]
    if missing_files:
        raise FileNotFoundError(f"Reference files ({', '.join(missing_files)}) are missing.")

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
    uploaded_markers = len(uploaded_map.find_all("circlemarker"))
    correct_markers = len(correct_map.find_all("circlemarker"))
    if uploaded_markers >= correct_markers:
        grade += 10

    # Verify marker colors and popup data (placeholder logic)
    grade += 10  # Placeholder for successful verification

    # 6. Bar Chart Grading (15 Points)
    try:
        # Compare chart structure using grayscale SSIM
        uploaded_image = np.array(Image.open(uploaded_png).convert("L"))
        correct_image = np.array(Image.open(correct_png).convert("L"))
        similarity_score = ssim(uploaded_image, correct_image)

        if similarity_score > 0.9:  # High similarity
            grade += 10
        elif similarity_score > 0.7:  # Moderate similarity
            grade += 7
        else:
            grade += 5

        # Validate bar chart labels using OCR
        uploaded_text = pytesseract.image_to_string(uploaded_png)
        required_labels = ["4.0-4.5", "4.5-5.0", ">5.0"]
        if all(label in uploaded_text for label in required_labels):
            grade += 5
        else:
            grade += 3  # Partial points if some labels are missing
    except Exception as e:
        print(f"Error grading bar chart: {e}")
        grade += 0  # No points if the bar chart fails

    # 7. Text Summary Grading (15 Points)
    try:
        # Load the uploaded and correct CSV files
        uploaded_summary = pd.read_csv(uploaded_csv)
        correct_summary = pd.read_csv(correct_csv)

        # Compare numerical values regardless of column names
        uploaded_values = uploaded_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()
        correct_values = correct_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()

        # Check for small tolerance in values
        tolerance = 0.01
        matching_values = sum(abs(u - c) <= tolerance for u, c in zip(uploaded_values, correct_values))
        grade += (15 * matching_values / len(correct_values))  # Scale points by percentage match
    except Exception as e:
        print(f"Error grading CSV: {e}")
        grade += 0  # No points if the CSV comparison fails

    return round(grade)
