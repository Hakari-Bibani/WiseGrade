import pandas as pd
import re
import os
import json
import requests
from io import StringIO
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
import pytesseract
from Levenshtein import ratio

def grade_assignment(code, html_path, png_path, csv_path):
    grade = 0
    # --- Evaluate Code (50 points) ---
    grade += evaluate_code(code)

    # --- Evaluate Uploaded Files (50 points) ---
    grade += evaluate_uploaded_files(html_path, png_path, csv_path)

    return round(grade)


def evaluate_code(code):
    code_grade = 0

    # 1. Library Imports (20 Points)
    required_imports = ["folium", "matplotlib", "requests", "pandas", "seaborn", "urllib"]
    imported_libraries = [lib for lib in required_imports if lib in code]
    code_grade += min(10, len(imported_libraries)*2)

    if "import" in code:
      code_grade += 2 #proper import organization and no unused

    # 2. Code Quality (20 Points)
    #   Variable Naming (5 Points)
    if re.search(r'(earthquake_map|magnitude_counts)', code):
       code_grade += 5
    #   Spacing (5 Points)
    if re.search(r'=\s', code) and re.search(r'>\s', code) and re.search(r'<\s', code) :
       code_grade += 5

    # 3. Fetching Data from the API (10 Points)
    api_url_pattern = r'https://earthquake\.usgs\.gov/fdsnws/event/1/query\?format=geojson&starttime=\d{4}-\d{2}-\d{2}&endtime=\d{4}-\d{2}-\d{2}'
    if re.search(api_url_pattern, code):
         code_grade += 5

    if "response.status_code" in code:
        code_grade += 5

    # 4. Filtering Earthquakes (10 Points)
    if re.search(r'magnitude\s*>\s*4\.0', code):
       code_grade += 5
    if re.search(r'(latitude|longitude|magnitude|time)', code, re.IGNORECASE):
        code_grade += 5

    return code_grade


def evaluate_uploaded_files(html_path, png_path, csv_path):
    file_grade = 0

    # 5. Map Visualization (20 Points)
    file_grade += evaluate_map(html_path)

    # 6. Bar Chart (15 Points)
    file_grade += evaluate_chart(png_path)

    # 7. Text Summary (15 Points)
    file_grade += evaluate_summary(csv_path)

    return file_grade


def evaluate_map(html_path):
    map_grade = 0
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Check for marker colors (green, yellow, red)
        if '"color": "green"' in html_content:
            map_grade += 3
        if '"color": "yellow"' in html_content:
            map_grade += 3
        if '"color": "red"' in html_content:
             map_grade += 3
         # Check for popups
        if re.search(r'popup=\s*".*magnitude.*"', html_content, re.IGNORECASE):
           map_grade += 3
        if re.search(r'popup=\s*".*latitude.*longitude.*"', html_content, re.IGNORECASE):
            map_grade += 4
        if re.search(r'popup=\s*".*time.*"', html_content, re.IGNORECASE):
           map_grade += 4

    except Exception as e:
        print(f"Error evaluating map: {e}")

    return map_grade

def evaluate_chart(png_path):
  chart_grade = 0
  try:
    # Load images
    uploaded_image = cv2.imread(png_path)
    expected_image = cv2.imread('utils/expected_chart.png') # expected chart

    if uploaded_image is None or expected_image is None:
        return 0  # Return 0 points if images can't be loaded

    # Convert images to grayscale
    uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
    expected_gray = cv2.cvtColor(expected_image, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detector
    uploaded_edges = cv2.Canny(uploaded_gray, 100, 200)
    expected_edges = cv2.Canny(expected_gray, 100, 200)

    # Structural Similarity Comparison
    if uploaded_edges.size == expected_edges.size and uploaded_edges.shape == expected_edges.shape:
      similarity_score = ssim(uploaded_edges, expected_edges)
      chart_grade += max(0, min(10, similarity_score * 10))  # Map similarity score to points

    # Text Extraction and Comparison (OCR)
    try:
        uploaded_text = pytesseract.image_to_string(uploaded_gray).strip()
        expected_text = pytesseract.image_to_string(expected_gray).strip()
        text_similarity = ratio(uploaded_text, expected_text)
        chart_grade += max(0, min(5, text_similarity * 5))
    except Exception as e:
        print(f"Error with OCR text extraction: {e}")

  except Exception as e:
    print(f"Error evaluating chart: {e}")
  return chart_grade


def evaluate_summary(csv_path):
    summary_grade = 0
    try:
        uploaded_df = pd.read_csv(csv_path)
        expected_df = pd.read_csv('utils/expected_summary.csv')  # expected csv

        if uploaded_df.empty or expected_df.empty:
            return 0

        uploaded_values = uploaded_df.values.flatten().astype(str)
        expected_values = expected_df.values.flatten().astype(str)

        # Calculate similarity between value sets (ignoring order)
        common_values = sum(1 for val in uploaded_values if val in expected_values)
        total_values = max(len(uploaded_values), len(expected_values))
        similarity_score = common_values / total_values if total_values > 0 else 0

        summary_grade += max(0, min(15, similarity_score * 15))  # Scale score to 15 points

    except Exception as e:
         print(f"Error evaluating summary CSV: {e}")
    return summary_grade
