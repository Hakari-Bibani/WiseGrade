import re
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os


def grade_assignment(code, uploaded_html=None, uploaded_png=None, uploaded_csv=None):
    """
    Grade Assignment 2 based on pasted code and uploaded files.
    """

    grade = 0

    ### Part 1: Evaluate the Code

    # 1. Library Imports (20 Points)
    required_imports = ["folium", "matplotlib", "seaborn", "requests", "urllib", "pandas"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    unused_imports = re.findall(r"import\s+(\w+)", code)  # Find all imported libraries
    unused_imports = [lib for lib in unused_imports if lib not in code or lib not in required_imports]

    if imported_libraries == len(required_imports) and not unused_imports:
        grade += 20
    else:
        grade += max(0, imported_libraries * 4 - len(unused_imports))  # Deduct for unused imports

    # 2. Code Quality (10 Points)
    code_quality_score = 10
    if any(re.match(r"\s*[a-z]\s*=", line) for line in code.split("\n")):
        code_quality_score -= 2  # Deduct for single-letter variables
    if "=" in code.replace(" = ", ""):
        code_quality_score -= 2  # Deduct for missing spacing
    if "#" not in code:
        code_quality_score -= 2  # Deduct for missing comments
    if "\n\n" not in code:
        code_quality_score -= 2  # Deduct for poor organization
    grade += max(0, code_quality_score)

    # 3. Fetching Data from the API (10 Points)
    api_score = 0
    if "https://earthquake.usgs.gov/fdsnws/event/1/query" in code:
        api_score += 5  # Correct API URL
    if "response.status_code" in code:
        api_score += 5  # Proper error handling
    grade += api_score

    # 4. Filtering Earthquakes (10 Points)
    filtering_score = 0
    if "magnitude > 4.0" in code:
        filtering_score += 5  # Correct filtering logic
    if all(field in code for field in ["latitude", "longitude", "magnitude", "time"]):
        filtering_score += 5  # Proper data extraction
    grade += filtering_score

    ### Part 2: Evaluate the Uploaded Files

    # 5. Map Visualization (20 Points)
    if uploaded_html:
        with open(uploaded_html, "r") as html_file:
            html_content = BeautifulSoup(html_file, "html.parser")
            markers = html_content.find_all("marker")
            if markers and any("green" in str(marker) for marker in markers) and \
                    any("yellow" in str(marker) for marker in markers) and \
                    any("red" in str(marker) for marker in markers):
                grade += 20  # Full points for valid markers and popups

    # 6. Bar Chart (15 Points)
    if uploaded_png:
        try:
            uploaded_image = np.array(Image.open(uploaded_png).convert("L"))
            grade += 12  # Add fixed score if the PNG is present
        except Exception:
            pass

    # 7. Text Summary (15 Points)
    correct_values = {
        "Total Earthquakes": 210.0,
        "Average Magnitude": 4.64,
        "Maximum Magnitude": 7.1,
        "Minimum Magnitude": 4.1,
        "4.0-4.5": 109.0,
        "4.5-5.0": 76.0,
        ">5.0": 25.0
    }

    if uploaded_csv:
        try:
            uploaded_data = pd.read_csv(uploaded_csv, header=None).values.flatten()
            uploaded_values = [float(val) for val in uploaded_data if isinstance(val, (float, int))]
            correct_uploaded = all(
                abs(uploaded_values[i] - list(correct_values.values())[i]) < 0.01
                for i in range(len(correct_values))
            )
            if correct_uploaded:
                grade += 15
        except Exception:
            pass

    return round(grade)


# For testing purposes
if __name__ == "__main__":
    # Replace with actual file paths for testing
    student_code = """
    import requests
    import pandas as pd
    import folium
    import matplotlib.pyplot as plt
    # Dummy code example
    """
    uploaded_html = "uploaded_map.html"
    uploaded_png = "uploaded_chart.png"
    uploaded_csv = "uploaded_summary.csv"

    # Grade the assignment
    try:
        final_score = grade_assignment(student_code, uploaded_html, uploaded_png, uploaded_csv)
        print(f"Student's Grade: {final_score}/100")
    except Exception as e:
        print(f"Error: {e}")
