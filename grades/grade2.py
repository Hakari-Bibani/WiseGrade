import pandas as pd
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
        print(f"Missing reference files: {missing_files}")
        return 0  # Cannot proceed without reference files

    grade = 0

    # 1. Library Imports (10 Points)
    required_imports = ["folium", "matplotlib", "requests", "pandas"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    library_imports_score = min(10, imported_libraries * 2)
    print(f"Library Imports Score: {library_imports_score}/10")
    grade += library_imports_score

    # 2. Code Quality (20 Points)
    code_quality_deductions = 0
    if any(len(var) == 1 and var.isalpha() for var in code.split("\n")):
        code_quality_deductions += 1  # Deduct for single-letter variables
    if "=" in code.replace(" = ", ""):
        code_quality_deductions += 1  # Deduct for missing spacing
    if "#" not in code:
        code_quality_deductions += 1  # Deduct for missing comments
    if "\n\n" not in code:
        code_quality_deductions += 1  # Deduct for poor organization
    code_quality_score = max(0, 20 - code_quality_deductions * 5)
    print(f"Code Quality Score: {code_quality_score}/20")
    grade += code_quality_score

    # 3. Fetching Data from API (10 Points)
    fetching_data_score = 0
    if "https://earthquake.usgs.gov/fdsnws/event/1/query" in code:
        fetching_data_score += 3  # Correct API URL
    if "requests.get" in code:
        fetching_data_score += 3  # Correct API call
    if "response.status_code" in code:
        fetching_data_score += 4  # Proper error handling
    print(f"Fetching Data Score: {fetching_data_score}/10")
    grade += fetching_data_score

    # 4. Filtering Earthquakes (10 Points)
    filtering_data_score = 0
    if "magnitude > 4.0" in code:
        filtering_data_score += 5  # Correct filtering logic
    if all(field in code for field in ["latitude", "longitude", "magnitude", "time"]):
        filtering_data_score += 5  # Proper data extraction
    print(f"Filtering Data Score: {filtering_data_score}/10")
    grade += filtering_data_score

    # 5. Map Visualization (20 Points)
    try:
        with open(uploaded_html, "r") as f:
            uploaded_map = BeautifulSoup(f, "html.parser")
        with open(correct_html, "r") as f:
            correct_map = BeautifulSoup(f, "html.parser")

        uploaded_markers = len(uploaded_map.find_all("circlemarker"))
        correct_markers = len(correct_map.find_all("circlemarker"))

        if uploaded_markers >= correct_markers:
            map_score = 20
        else:
            map_score = 10  # Deduct for missing markers
        print(f"Uploaded markers: {uploaded_markers}, Correct markers: {correct_markers}")
        print(f"Map Visualization Score: {map_score}/20")
        grade += map_score
    except Exception as e:
        print(f"Error grading map visualization: {e}")

    # 6. Bar Chart Grading (15 Points)
    try:
        uploaded_image = np.array(Image.open(uploaded_png).convert("L"))
        correct_image = np.array(Image.open(correct_png).convert("L"))
        similarity_score = ssim(uploaded_image, correct_image)

        chart_score = 10 if similarity_score > 0.9 else 7 if similarity_score > 0.7 else 5
        print(f"Bar Chart SSIM Score: {similarity_score}")

        uploaded_text = pytesseract.image_to_string(uploaded_png)
        required_labels = ["4.0-4.5", "4.5-5.0", ">5.0"]
        label_score = 5 if all(label in uploaded_text for label in required_labels) else 3
        chart_score += label_score
        print(f"Bar Chart OCR Label Score: {label_score}/5")
        print(f"Bar Chart Total Score: {chart_score}/15")
        grade += chart_score
    except Exception as e:
        print(f"Error grading bar chart: {e}")

    # 7. Text Summary Grading (15 Points)
    try:
        uploaded_summary = pd.read_csv(uploaded_csv)
        correct_summary = pd.read_csv(correct_csv)

        uploaded_values = uploaded_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()
        correct_values = correct_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()

        tolerance = 0.01
        matching_values = sum(abs(u - c) <= tolerance for u, c in zip(uploaded_values, correct_values))
        csv_score = round(15 * matching_values / len(correct_values))
        print(f"Text Summary Matching Values: {matching_values}/{len(correct_values)}")
        print(f"Text Summary Score: {csv_score}/15")
        grade += csv_score
    except Exception as e:
        print(f"Error grading text summary: {e}")

    print(f"Final Grade: {grade}/100")
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
