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
    grade += check_map_visualization(code, html_path)

    # 6. Bar Chart (15 points)
    grade += check_bar_chart(png_path)
    grade += check_bar_chart(code, png_path)

    # 7. Text Summary (15 points)
    grade += check_text_summary(csv_path)
@@ -102,80 +102,75 @@
     logging.info(f"Earthquake Filtering Grade: {grade}")
     return grade

def check_map_visualization(html_path):
def check_map_visualization(code, html_path):
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
        # Correct Colors check
        correct_colors = ['green', 'yellow', 'red']
        student_colors = [marker.find('img').get('src') for marker in student_markers]
        # Check if colors of the student marker are in correct colors set
        if any(color not in str(student_colors) for color in correct_colors):
            logging.info(f"Incorrect colors found in student map: {student_colors}")
            return 0 # fail color check
        else:
            grade += 10
            
           grade += 10
        # popup text check: the text includes the time magnitude location
        student_popups = student_soup.find_all("div", class_="leaflet-popup-content")
        if all(any(keyword in str(popup) for keyword in ["magnitude", "location","time"]) for popup in student_popups):
            grade += 5
             grade += 10
        else:
            logging.info(f"Incorrect popups found in student map: {student_popups}")
        
        logging.info(f"Map Visualization Grade: {grade}")
             logging.info(f"Incorrect popups found in student map: {student_popups}")
       

    except Exception as e:
        logging.error(f"Error comparing HTML files: {e}")
        return 0

    logging.info(f"Map Visualization Grade: {grade}")
    return grade

def check_bar_chart(png_path):
def check_bar_chart(code, png_path):
    grade = 0
    try:
        student_image = Image.open(png_path).convert("RGB")
        correct_image = Image.open(os.path.join("grades", "correct_chart.png")).convert("RGB")
         # Execute code to get the chart
        local_context = {}
        exec(code, {}, local_context)
        bar_chart_figure = next((obj for obj in local_context.values() if isinstance(obj, plt.Figure)), None)
        if not bar_chart_figure:
            logging.info("No bar chart found when executing the student code.")
            return 0

        student_array = np.array(student_image)
        correct_array = np.array(correct_image)
        if student_array.shape != correct_array.shape:
            logging.info(f"Image shapes are different, student {student_array.shape}, correct {correct_array.shape}")
            return 0 # fail if the shape of images are not the same
        # Calculate the Bar Charts Properties
        ax = bar_chart_figure.axes[0]
        bar_heights = ax.patches
        tick_labels = ax.get_xticklabels()

        score = ssim(student_array, correct_array, channel_axis=2)
        logging.info(f"SSIM score: {score}")
        if score > 0.85:
            grade += 15
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
@@ -188,19 +183,25 @@
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
