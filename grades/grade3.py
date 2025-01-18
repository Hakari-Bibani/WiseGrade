import os
import pandas as pd

# Path to the correct Excel file in the repository
CORRECT_EXCEL_PATH = "correct_files/correct_assignment3.xlsx"

def grade_assignment(code, html_path, excel_path):
    """
    Grades Assignment 3 based on the provided code, HTML file, and Excel file.
    Returns a numerical grade (0-100).
    """

    total_score = 0

    #### Part 1: Code Grading ####
    
    ## 1. Library Imports
    lib_points = 0
    # gspread/pygsheets/google-api-python-client (8 points)
    if any(lib in code for lib in ["gspread", "pygsheets", "google-api-python-client"]):
        lib_points += 8
    # pandas/numpy (4 points)
    if any(lib in code for lib in ["pandas", "numpy"]):
        lib_points += 4
    # folium/plotly/geopandas/mapping matplotlib (8 points)
    if any(lib in code for lib in ["folium", "plotly", "geopandas", "matplotlib"]):
        lib_points += 8
    total_score += lib_points

    ## 2. Code Quality
    quality_points = 0
    # Check for Descriptive Variable Names (5 points)
    descriptive_keywords = ["student_id", "code_input", "temperature", "longitude", "latitude"]
    if any(word in code for word in descriptive_keywords):
        quality_points += 5
    # Check for proper spacing (5 points)
    if " = " in code:
        quality_points += 5
    # Check for comments (5 points)
    if "#" in code:
        quality_points += 5
    # Check for organization (5 points) – e.g., multiple functions
    if code.count("def ") >= 3:
        quality_points += 5
    total_score += quality_points

    ## 3. JSON Path (10 Points)
    if "json_path" in code:
        total_score += 10

    ## 4. Sheet Creation (5 Points Each)
    if "Below_25" in code:
        total_score += 5
    if "Above_25" in code:
        total_score += 5

    #### Part 2: HTML File Grading ####
    html_points = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read().lower()
            # Check for blue and red data points
            if "blue" in html_content:
                html_points += 10
            if "red" in html_content:
                html_points += 10
    except Exception as e:
        print(f"Error reading HTML file: {e}")
    total_score += html_points

    #### Part 3: Excel File Grading ####
    excel_points = 0
    try:
        # Load the correct Excel file
        correct_xl = pd.ExcelFile(CORRECT_EXCEL_PATH)
        correct_sheets = correct_xl.sheet_names

        # Load the submitted Excel file
        submitted_xl = pd.ExcelFile(excel_path)
        submitted_sheets = submitted_xl.sheet_names

        # Compare Sheet Names (10 points)
        if set(correct_sheets) == set(submitted_sheets):
            excel_points += 10

        # Compare Column Names (10 points)
        for sheet in correct_sheets:
            if sheet in submitted_sheets:
                correct_df = correct_xl.parse(sheet)
                submitted_df = submitted_xl.parse(sheet)
                if list(correct_df.columns) == list(submitted_df.columns):
                    excel_points += 10
                    break

        # Compare Data (10 points)
        for sheet in correct_sheets:
            if sheet in submitted_sheets:
                correct_df = correct_xl.parse(sheet)
                submitted_df = submitted_xl.parse(sheet)
                if correct_df.equals(submitted_df):
                    excel_points += 10
                    break
    except Exception as e:
        print(f"Error processing Excel file: {e}")
    total_score += excel_points

    # Ensure the total score does not exceed 100
    return min(total_score, 100)
