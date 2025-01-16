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
    grade += check_map_visualization(code, html_path)

    # 6. Bar Chart (15 points)
    grade += check_bar_chart(code, png_path)

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

def check_map_visualization(code, html_path):
    grade = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            student_html = f.read()
        
        student_soup = BeautifulSoup(student_html, "html.parser")

        student_markers = student_soup.find_all("div", class_="leaflet-marker-icon")

        # Check if any markers exist.
        if not student_markers:
            logging.info("No markers found in student map, failing map visualization check")
            return 0  # No markers found, fail the map visualization check
        
        # Correct Colors check
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
             grade += 10
        else:
             logging.info(f"Incorrect popups found in student map: {student_popups}")
       
        
    except Exception as e:
        logging.error(f"Error comparing HTML files: {e}")
        return 0
    
    logging.info(f"Map Visualization Grade: {grade}")
    return grade

def check_bar_chart(code, png_path):
    grade = 0
    try:
         # Execute code to get the chart
        local_context = {}
        exec(code, {}, local_context)
        bar_chart_figure = next((obj for obj in local_context.values() if isinstance(obj, plt.Figure)), None)
        if not bar_chart_figure:
            logging.info("No bar chart found when executing the student code.")
            return 0
        
        # Calculate the Bar Charts Properties
        ax = bar_chart_figure.axes[0]
        bar_heights = ax.patches
        tick_labels = ax.get_xticklabels()
        
        # Check the tick labels
        correct_labels = ["4.0-4.5", "4.5-5.0", "5.0+"]
        if [label.get_text() for label in tick_labels] != correct_labels:
              logging.info(f"Labels are not correct {tick_labels}")
              return 0
        
        # Check the bar heights if they are greater or less than zero
        if not all(height.get_height() > 0 for height in bar_heights):
              logging.info(f"Bar heights are not correct {bar_heights}")
              return 0
        
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

        # Check that both dataframes have the same number of rows and columns
        if student_df.shape != correct_df.shape:
            logging.info(f"Dataframes shape not matching {student_df.shape} vs {correct_df.shape}")
            return 0
        
        # Check each column one by one
        for col in correct_df.columns:
          if not col in student_df.columns:
            logging.info(f"Column {col} is not in student dataframe")
            return 0
          if not student_df[col].equals(correct_df[col]):
            logging.info(f"Column {col} is not equal in student dataframe vs correct dataframe")
            return 0
        
        grade += 15

    except Exception as e:
        logging.error(f"Error comparing CSV files: {e}")
        return 0
    logging.info(f"Text Summary Grade: {grade}")
    return grade
