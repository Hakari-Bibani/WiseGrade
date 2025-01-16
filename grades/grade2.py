import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
import re
from skimage.metrics import structural_similarity as ssim
import io
import matplotlib.pyplot as plt
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def grade_assignment(code, html_path, png_path, csv_path):
    grade = 0

    # 1. Library Imports (10 points)
    grade += check_library_imports(code)

    # 2. Code Quality (20 points)
    grade += check_code_quality(code)

    # 3. Fetching Data from API (10 points)
    grade += check_api_fetching(code)

    # 4. Filtering Earthquakes (10 points)
    grade += check_earthquake_filtering(code)

    # 5. Map Visualization (20 points)
    grade += check_map_visualization(html_path)

    # 6. Bar Chart (15 points)
    grade += check_bar_chart(png_path)

    # 7. Text Summary (15 points)
    grade += check_text_summary(csv_path)
    logging.info(f"Final Grade: {grade}")
    return round(grade)

def check_library_imports(code):
    grade = 0
    required_imports = ["folium", "matplotlib", "seaborn", "requests", "urllib", "pandas"]
    imported_libraries = [lib for lib in required_imports if lib in code]
    
    # Check if there is any unused import
    for line in code.splitlines():
        if line.startswith("import") or line.startswith("from"):
            import_name = line.replace("import ", "").replace("from ", "").split(" ")[0].split(".")[0].strip()
            if import_name not in required_imports:
                logging.info(f"Unused import found {import_name} in code, failed library import check")
                return 0 # Fail on unused import
        
    grade += min(10,len(imported_libraries) * (10 / len(required_imports)))
    logging.info(f"Library Imports Grade: {grade}")
    return grade

def check_code_quality(code):
    grade = 0
    code_quality_issues = 0

    # Variable Naming
    if re.search(r'\b[a-z]\s*=', code) and not re.search(r'\b[a-z]+[_a-z]+\s*=', code):
        code_quality_issues += 1 # Use of single-letter variable name

    # Spacing
    if any(f" {char} =" in code or f" {char}=" in code for char in "=><"):
        code_quality_issues += 1  # Missing space after operator
    if any(f"{char} =" in code or f"{char}=" in code for char in "=><"):
        code_quality_issues +=1 # Inconsistent spacing

    # Comments
    if "#" not in code:
        code_quality_issues += 1

    # Code organization
    if "\n\n" not in code:
         code_quality_issues += 1

    grade += max(0, 20 - code_quality_issues * (20 / 4))
    logging.info(f"Code Quality Grade: {grade}")
    return grade

def check_api_fetching(code):
    grade = 0
    # Checks for a valid url and proper error handling
    api_url_pattern = re.compile(r"https?://earthquake\.usgs\.gov/fdsnws/event/1/query\?format=geojson&starttime=\d{4}-\d{2}-\d{2}&endtime=\d{4}-\d{2}-\d{2}")
    if api_url_pattern.search(code):
      grade += 5
    if "response.status_code" in code:
      grade += 5
    logging.info(f"API Fetching Grade: {grade}")
    return grade

def check_earthquake_filtering(code):
     grade = 0
     if "magnitude" in code and "> 4.0" in code:
         grade += 10
     if "latitude" in code and "longitude" in code and "time" in code:
         grade += 10
     logging.info(f"Earthquake Filtering Grade: {grade}")
     return grade


def check_map_visualization(html_path):
    grade = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            student_html = f.read()
        with open(os.path.join("grades", "correct_map.html"), "r", encoding="utf-8") as f:
            correct_html = f.read()

        # save the read html files for debugging purposes
        with open("grades/student_map.html", "w", encoding="utf-8") as f:
            f.write(student_html)
        with open("grades/correct_map.html", "w", encoding="utf-8") as f:
            f.write(correct_html)
        
        student_soup = BeautifulSoup(student_html, "html.parser")
        correct_soup = BeautifulSoup(correct_html, "html.parser")

        student_markers = student_soup.find_all("div", class_="leaflet-marker-icon")
        correct_markers = correct_soup.find_all("div", class_="leaflet-marker-icon")

        # Check if any markers exist.
        if not student_markers:
            logging.info("No markers found in student map, failing map visualization check")
            return 0  # No markers found, fail the map visualization check
        
        # Markers count
        if len(student_markers) == len(correct_markers):
           grade += 5
        else:
           logging.info(f"Incorrect marker counts, student: {len(student_markers)}, correct: {len(correct_markers)}")
        
        # Colors check
        correct_colors = ['green', 'yellow', 'red']
        student_colors = [marker.find('img').get('src') for marker in student_markers]
        # Check if colors of the student marker are in correct colors set
        if any(color not in str(student_colors) for color in correct_colors):
            logging.info(f"Incorrect colors found in student map: {student_colors}")
            return 0 # fail color check
        else:
            grade += 10
            
        # popup text check: the text includes the time magnitude location
        student_popups = student_soup.find_all("div", class_="leaflet-popup-content")
        if all(any(keyword in str(popup) for keyword in ["magnitude", "location","time"]) for popup in student_popups):
            grade += 5
        else:
            logging.info(f"Incorrect popups found in student map: {student_popups}")
        
        logging.info(f"Map Visualization Grade: {grade}")
        
    except Exception as e:
        logging.error(f"Error comparing HTML files: {e}")
        return 0
    
    return grade

def check_bar_chart(png_path):
    grade = 0
    try:
        student_image = Image.open(png_path).convert("RGB")
        correct_image = Image.open(os.path.join("grades", "correct_chart.png")).convert("RGB")
        
        student_array = np.array(student_image)
        correct_array = np.array(correct_image)

        if student_array.shape != correct_array.shape:
            logging.info(f"Image shapes are different, student {student_array.shape}, correct {correct_array.shape}")
            return 0 # fail if the shape of images are not the same
        
        score = ssim(student_array, correct_array, channel_axis=2)
        logging.info(f"SSIM score: {score}")
        if score > 0.85:
            grade += 15
        
    except Exception as e:
        logging.error(f"Error comparing image files: {e}")
        return 0
    logging.info(f"Bar Chart Grade: {grade}")
    return grade

def check_text_summary(csv_path):
    grade = 0
    try:
        student_df = pd.read_csv(csv_path)
        correct_df = pd.read_csv(os.path.join("grades", "correct_summary.csv"))
        if student_df.equals(correct_df):
           grade += 15
        else:
          logging.info("Dataframes are not equal, failing text summary check")
          # Detailed comparison
          diff_mask = (student_df != correct_df)
          diff_loc = np.where(diff_mask)
          if not diff_loc[0].size == 0:
              logging.info(f"Differences at rows {diff_loc[0]}, cols {diff_loc[1]}")
              for row, col in zip(*diff_loc):
                  logging.info(f"Student Value: {student_df.iloc[row, col]}, Correct Value: {correct_df.iloc[row, col]}")
    except Exception as e:
        logging.error(f"Error comparing CSV files: {e}")
        return 0
    logging.info(f"Text Summary Grade: {grade}")
    return grade
