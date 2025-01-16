import pandas as pd
import re
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import pytesseract


def grade_assignment(code, uploaded_html, uploaded_png, uploaded_csv):
    """
    Grade Assignment 2 based on the script and uploaded files.
    """

    # Initialize grade
    grade = 0

    # PART 1: Evaluate the script (50 Points)
    
    # 1. Library Imports (20 Points)
    required_imports = ["folium", "matplotlib", "requests", "pandas"]
    library_imports_score = 0
    for lib in required_imports:
        if lib in code:
            library_imports_score += 5  # 5 points per correct library
    if any(lib not in required_imports for lib in re.findall(r"import\s+(\w+)", code)):
        library_imports_score -= 2  # Deduct 2 points for unused imports
    grade += min(20, library_imports_score)

    # 2. Code Quality (20 Points)
    # Check variable naming
    variable_naming_score = 5 if all(len(var) > 2 for var in re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", code)) else 3
    # Check spacing
    spacing_score = 5 if " =" not in code and "= " not in code else 3
    grade += variable_naming_score + spacing_score

    # 3. Fetching Data (10 Points)
    fetching_data_score = 0
    if "https://earthquake.usgs.gov/fdsnws/event/1/query" in code:
        fetching_data_score += 5  # Correct API URL
    if "response.status_code" in code:
        fetching_data_score += 5  # Proper error handling
    grade += fetching_data_score

    # PART 2: Evaluate the uploaded files (50 Points)

    # 4. Map Visualization (20 Points)
    map_score = 0
    try:
        with open(uploaded_html, "r") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")

        # Check marker colors
        popups = soup.find_all("popup")
        popup_content = " ".join(popup.text for popup in popups)
        green_marker = any("green" in marker.attrs.get("style", "").lower() for marker in soup.find_all("marker"))
        yellow_marker = any("yellow" in marker.attrs.get("style", "").lower() for marker in soup.find_all("marker"))
        red_marker = any("red" in marker.attrs.get("style", "").lower() for marker in soup.find_all("marker"))

        if green_marker:
            map_score += 3
        if yellow_marker:
            map_score += 3
        if red_marker:
            map_score += 3

        # Check popups
        if re.search(r"magnitude", popup_content, re.IGNORECASE):
            map_score += 3
        if re.search(r"latitude|longitude", popup_content, re.IGNORECASE):
            map_score += 4
        if re.search(r"\d{4}-\d{2}-\d{2}", popup_content):  # Check for readable time
            map_score += 4
    except Exception as e:
        print(f"Error evaluating map: {e}")

    grade += map_score

    # 5. Bar Chart (15 Points)
    bar_chart_score = 0
    try:
        # Check if PNG exists
        uploaded_image = Image.open(uploaded_png)

        # Use OCR to extract text and check if key labels are present
        extracted_text = pytesseract.image_to_string(uploaded_png)
        if all(label in extracted_text for label in ["4.0-4.5", "4.5-5.0", ">5.0"]):
            bar_chart_score += 10  # Text-based validation of ranges
        else:
            bar_chart_score += 5  # Partial score if ranges are missing
    except Exception as e:
        print(f"Error evaluating bar chart: {e}")

    grade += bar_chart_score

    # 6. Text Summary (15 Points)
    text_summary_score = 0
    try:
        # Load the uploaded CSV
        uploaded_csv = pd.read_csv(uploaded_csv)

        # Define correct answers
        correct_values = {
            "Total Earthquakes": 210.0,
            "Average Magnitude": 4.64,
            "Maximum Magnitude": 7.1,
            "Minimum Magnitude": 4.1,
            "4.0-4.5": 109.0,
            "4.5-5.0": 76.0,
            ">5.0": 25.0,
        }

        # Check for matches regardless of column names
        uploaded_values = uploaded_csv.select_dtypes(include=["float", "int"]).to_numpy().flatten()
        correct_values_list = list(correct_values.values())

        # Compare values with a tolerance
        matching_values = sum(abs(u - c) <= 0.01 for u, c in zip(uploaded_values, correct_values_list))
        text_summary_score += (15 * matching_values / len(correct_values_list))  # Scale points based on percentage match
    except Exception as e:
        print(f"Error evaluating text summary: {e}")

    grade += text_summary_score

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
