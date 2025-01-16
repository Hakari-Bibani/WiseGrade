import ast
import pandas as pd
import re
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import pytesseract
import os


def check_library_imports(code):
    """
    Parses the student's code using AST to check for required library imports.
    """
    required_imports = {"folium", "matplotlib", "seaborn", "requests", "urllib", "pandas"}
    imported_libraries = set()

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_libraries.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imported_libraries.add(node.module)
    except SyntaxError as e:
        return 0, f"Syntax error in code: {e}"

    score = len(imported_libraries.intersection(required_imports)) * 2  # 2 points per library
    return min(score, 10), imported_libraries


def check_code_quality(code):
    """
    Checks for general code quality issues like poor variable naming,
    missing spaces around operators, lack of comments, and poor organization.
    """
    deductions = 0

    # Check for single-letter variables
    single_letter_vars = re.findall(r"\b[a-zA-Z]\b\s*=", code)
    deductions += len(single_letter_vars)

    # Check for missing spaces around "="
    missing_spaces = re.findall(r"[^ ]=[^ =]", code)
    deductions += len(missing_spaces)

    # Check for comments
    if code.count("#") < 5:  # Arbitrary threshold for minimum comments
        deductions += 2

    # Check for organization (e.g., missing blank lines between sections)
    if "\n\n" not in code:
        deductions += 2

    return max(0, 20 - deductions)


def check_api_fetching(code):
    """
    Checks if the student's code correctly fetches data from the USGS Earthquake API.
    """
    score = 0

    # Check for correct API URL
    if "https://earthquake.usgs.gov/fdsnws/event/1/query" in code:
        score += 3

    # Check for correct request method
    if "requests.get" in code or "urllib.request" in code:
        score += 3

    # Check for error handling
    if "response.status_code" in code:
        score += 4

    return min(score, 10)


def check_earthquake_filtering(code):
    """
    Checks for the correct data filtering criteria and required fields.
    """
    score = 0

    # Check for magnitude filtering
    if "magnitude > 4.0" in code:
        score += 5

    # Check for required fields
    fields = ["latitude", "longitude", "magnitude", "time"]
    if all(field in code for field in fields):
        score += 5

    return score


def check_map_visualization(uploaded_html, correct_html):
    """
    Compares the uploaded HTML map with the reference map.
    """
    with open(uploaded_html, "r") as f1, open(correct_html, "r") as f2:
        uploaded_map = BeautifulSoup(f1, "html.parser")
        correct_map = BeautifulSoup(f2, "html.parser")

    uploaded_markers = len(uploaded_map.find_all("circlemarker"))
    correct_markers = len(correct_map.find_all("circlemarker"))

    return 10 if uploaded_markers >= correct_markers else 5


def check_bar_chart(uploaded_png, correct_png):
    """
    Compares the uploaded bar chart with the reference chart using SSIM.
    Uses OCR to validate the labels.
    """
    uploaded_image = np.array(Image.open(uploaded_png).convert("L"))
    correct_image = np.array(Image.open(correct_png).convert("L"))
    similarity_score = ssim(uploaded_image, correct_image)

    # OCR for labels
    uploaded_text = pytesseract.image_to_string(uploaded_png)
    required_labels = ["4.0-4.5", "4.5-5.0", ">5.0"]

    label_score = 5 if all(label in uploaded_text for label in required_labels) else 3

    return 10 if similarity_score > 0.9 else (7 if similarity_score > 0.7 else 5) + label_score


def check_csv_summary(uploaded_csv, correct_csv):
    """
    Compares the numerical values in the uploaded CSV with the reference CSV.
    """
    uploaded_summary = pd.read_csv(uploaded_csv)
    correct_summary = pd.read_csv(correct_csv)

    uploaded_values = uploaded_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()
    correct_values = correct_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()

    tolerance = 0.01
    matching_values = sum(abs(u - c) <= tolerance for u, c in zip(uploaded_values, correct_values))

    return (15 * matching_values) // len(correct_values)


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

    # Check each criterion and accumulate points
    library_imports_score, _ = check_library_imports(code)
    grade += library_imports_score

    grade += check_code_quality(code)
    grade += check_api_fetching(code)
    grade += check_earthquake_filtering(code)
    grade += check_map_visualization(uploaded_html, correct_html)
    grade += check_bar_chart(uploaded_png, correct_png)
    grade += check_csv_summary(uploaded_csv, correct_csv)

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
