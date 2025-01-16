import ast
import pandas as pd
import re
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import pytesseract
import os
import json
import requests
from io import StringIO

def grade_assignment(code, uploaded_html, uploaded_png, uploaded_csv):
    """
    Grades the assignment based on specific criteria, providing feedback.
    """

    # --- Setup ---
    base_dir = os.path.dirname(os.path.abspath(__file__)) #Important Change
    correct_html = os.path.join(base_dir, "correct_map.html")
    correct_png = os.path.join(base_dir, "correct_chart.png")
    correct_csv = os.path.join(base_dir, "correct_summary.csv")
    correct_json = os.path.join(base_dir, "correct_data.json")

    # Verify that all reference files exist
    missing_files = [file for file in [correct_html, correct_png, correct_csv, correct_json] if not os.path.exists(file)]
    if missing_files:
        raise FileNotFoundError(f"Reference files ({', '.join(missing_files)}) are missing.")
    
    print(f"Base directory: {base_dir}")
    print(f"HTML path: {correct_html}")
    print(f"PNG path: {correct_png}")
    print(f"CSV path: {correct_csv}")
    print(f"JSON path: {correct_json}")

    grade = 0
    feedback = []  # List to store feedback messages

    # --- 1. Library Imports (10 Points) ---
    grade_imports, feedback_imports = check_imports(code)
    grade += grade_imports
    feedback.extend(feedback_imports)

    # --- 2. Code Quality (10 Points) ---
    grade_quality, feedback_quality = check_code_quality(code)
    grade += grade_quality
    feedback.extend(feedback_quality)

    # --- 3. API Data Fetching (15 Points) ---
    grade_api, feedback_api = check_api_fetching(code, correct_json)
    grade += grade_api
    feedback.extend(feedback_api)

    # --- 4. Data Filtering (10 Points) ---
    grade_filtering, feedback_filtering = check_earthquake_filtering(code)
    grade += grade_filtering
    feedback.extend(feedback_filtering)

    # --- 5. Map Generation (20 Points) ---
    grade_map, feedback_map = check_map_visualization(uploaded_html, correct_html)
    grade += grade_map
    feedback.extend(feedback_map)

    # --- 6. Chart Generation (15 Points) ---
    grade_chart, feedback_chart = check_bar_chart(uploaded_png, correct_png)
    grade += grade_chart
    feedback.extend(feedback_chart)

    # --- 7. CSV Summary Generation (20 Points) ---
    grade_csv, feedback_csv = check_csv_summary(uploaded_csv, correct_csv)
    grade += grade_csv
    feedback.extend(feedback_csv)

    return round(grade), feedback

def check_imports(code):
        """Checks for required library imports using AST parsing"""
        required_imports = ["folium", "matplotlib", "seaborn", "requests", "urllib", "pandas"]
        feedback_imports = []
        grade = 0
        try:
            tree = ast.parse(code)
            imported_names = {
                alias.name for node in tree.body if isinstance(node, ast.Import) for alias in node.names
            } | {
                name.id for node in tree.body if isinstance(node, ast.ImportFrom) for name in node.names
            }
            
            imported_libs = [lib for lib in required_imports if lib in imported_names]
            grade = min(10, len(imported_libs) * 2)
            if not imported_libs:
                 feedback_imports.append("No imports found")
            else:
                 missing_imports = [lib for lib in required_imports if lib not in imported_libs]
                 if missing_imports:
                      feedback_imports.append(f"Missing imports: {', '.join(missing_imports)}")
            
        except SyntaxError:
             feedback_imports.append("Invalid Python Syntax. Unable to check Imports")
        return grade , feedback_imports



def check_code_quality(code):
    """ Checks for code quality violations """
    feedback_quality = []
    grade = 10 #Full Points
    deductions = 0
    #Checking for single-letter variables
    if any(re.match(r"\s*[a-z]\s*=", line) for line in code.split("\n")):
         deductions += 1  
         feedback_quality.append("Deducted points for single-letter variables.")
    
    #Check for spacing
    if "=" in code.replace(" = ", ""):
         deductions += 1
         feedback_quality.append("Deducted points for missing spacing around the equal sign.")

    # Check for comments
    if "#" not in code:
          deductions += 1
          feedback_quality.append("Deducted points for missing comments.")
    
    if "\n\n" not in code:
          deductions += 1
          feedback_quality.append("Deducted points for poor organization (missing newlines).")
    
    grade = max(0, 10 - deductions * 2)

    if deductions == 0:
      feedback_quality.append("No code quality violations found")
    return grade, feedback_quality
    


def check_api_fetching(code, correct_json):
    """Checks API URL, request method, and basic data structure."""
    grade = 0
    feedback_api = []
    correct_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    try:
        # 1. Check for API URL
        if correct_url in code:
          grade += 3
        else:
             feedback_api.append("Incorrect API URL")

        # 2. Check request method
        if "requests.get" in code:
           grade += 3
        elif "urllib.request" in code:
            grade += 3
        else:
           feedback_api.append("Missing API call")

        # 3. Check for error handling
        if "response.status_code" in code or "e.code" in code:
           grade += 4
        else:
             feedback_api.append("Missing error handling")

        # 4. Retrieve the data to verify the json
        
        if "requests.get" in code and correct_url in code:
              response = requests.get(correct_url)
              if response.status_code == 200:
                    student_data = response.json()
                    with open(correct_json, 'r') as correct_data:
                        correct_data = json.load(correct_data)

                        #Check if student data contains keys and items from correct data
                        if correct_data.keys() <= student_data.keys():
                             grade += 5 #Correct Structure
                             if 'features' in student_data:
                               if len(student_data['features']) > 0:
                                    grade+= 0 #More thorough checks are missing
                               else:
                                    feedback_api.append("The student data has no earthquake features. Make sure the API is correctly used")
                             else:
                                feedback_api.append("The student data should contains a `features` key")
                        else:
                             feedback_api.append("The API return has an incorrect json structure")
              else:
                    feedback_api.append("There was a problem while fetching the API Data")


    except Exception as e:
        feedback_api.append(f"Error during API check: {e}")
    return grade , feedback_api



def check_earthquake_filtering(code):
    """Checks for correct filtering logic using string search."""
    grade = 0
    feedback_filtering = []
    if "magnitude > 4.0" in code:
         grade += 5
    else:
         feedback_filtering.append("Incorrect filtering logic")

    if all(field in code for field in ["latitude", "longitude", "magnitude", "time"]):
        grade += 5
    else:
        missing_fields = [field for field in ["latitude", "longitude", "magnitude", "time"] if field not in code]
        feedback_filtering.append(f"Missing Data fields: {', '.join(missing_fields)}")
    return grade, feedback_filtering



def check_map_visualization(uploaded_html, correct_html):
  """Analyzes the map for markers and structure, compares with a reference"""
  grade = 0
  feedback_map = []
  try:
    with open(uploaded_html, "r") as html_file:
        uploaded_map = BeautifulSoup(html_file, "html.parser")
    with open(correct_html, "r") as correct_map_file:
        correct_map = BeautifulSoup(correct_map_file, "html.parser")
    
    #Verify number of markers
    uploaded_markers = len(uploaded_map.find_all("circlemarker"))
    correct_markers = len(correct_map.find_all("circlemarker"))

    if uploaded_markers >= correct_markers:
        grade += 10
    else:
         feedback_map.append("Incorrect number of markers")
    
    # Verify marker colors
    uploaded_colors = {marker.get('fill') for marker in uploaded_map.find_all("circlemarker")}
    correct_colors = {marker.get('fill') for marker in correct_map.find_all("circlemarker")}

    if uploaded_colors == correct_colors:
         grade += 10 # All colors are correct
    else:
        feedback_map.append("Incorrect marker colors")
        

  except Exception as e:
      feedback_map.append(f"Error during map analysis: {e}")
  return grade, feedback_map


def check_bar_chart(uploaded_png, correct_png):
  """Compares the bar chart visually (SSIM) and verifies labels."""
  grade = 0
  feedback_chart = []
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
            missing_labels = [label for label in required_labels if label not in uploaded_text]
            feedback_chart.append(f"Missing labels: {', '.join(missing_labels)}")
            grade += 3  # Partial points if some labels are missing

  except Exception as e:
      feedback_chart.append(f"Error during chart analysis: {e}")
  return grade , feedback_chart
    

def check_csv_summary(uploaded_csv, correct_csv):
    """Checks the CSV content, focusing on data values, not column names."""
    grade = 0
    feedback_csv = []
    try:
        # Load the uploaded and correct CSV files
        uploaded_summary = pd.read_csv(uploaded_csv)
        correct_summary = pd.read_csv(correct_csv)

        if uploaded_summary.shape == correct_summary.shape:
            grade += 5 # Points for correct shape
            if not uploaded_summary.empty:
                 # Compare numerical values regardless of column names
                 uploaded_values = uploaded_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()
                 correct_values = correct_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()

                # Check for small tolerance in values
                 tolerance = 0.01
                 if len(uploaded_values) == len(correct_values):
                    matching_values = sum(abs(u - c) <= tolerance for u, c in zip(uploaded_values, correct_values))
                    grade += (15 * matching_values / len(correct_values))  # Scale points by percentage match
                 else:
                   feedback_csv.append("Incorrect Number of rows in CSV")

            else:
                feedback_csv.append("The summary file is empty")
        else:
          feedback_csv.append("Incorrect number of rows and columns")
    except Exception as e:
        feedback_csv.append(f"Error during csv analysis: {e}")
    return grade, feedback_csv
