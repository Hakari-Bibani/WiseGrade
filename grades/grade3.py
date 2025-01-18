import os
import pandas as pd

def grade_assignment(code, html_path, excel_path, correct_excel_path):
    """
    Grades Assignment 3 based on the provided code, HTML file, and Excel file.
    Returns a numerical grade (0-100).
    """

    total_score = 0

    #### Part 1: Code Grading (50 Points Total) ####

    ## 1. Library Imports (20 Points):
    lib_points = 0
    # Check for gspread/pygsheets/google-api-python-client (8 pts)
    if any(lib in code for lib in ["gspread", "pygsheets", "google-api-python-client"]):
        lib_points += 8
    # Check for pandas/numpy (4 pts)
    if any(lib in code for lib in ["pandas", "numpy"]):
        lib_points += 4
    # Check for folium/plotly/geopandas/matplotlib (8 pts)
    if any(lib in code for lib in ["folium", "plotly", "geopandas", "matplotlib"]):
        lib_points += 8
    total_score += lib_points

    ## 2. Code Quality (20 Points):
    quality_points = 0
    # Descriptive Variable Names (5 pts): Simple heuristic
    if any(keyword in code for keyword in ["student_id", "temperature", "longitude", "latitude", "json_path"]):
        quality_points += 5
    # Spacing (5 pts): Check for " = " as heuristic
    if " = " in code:
        quality_points += 5
    # Comments (5 pts): Check for at least 3 occurrences of "#"
    if code.count("#") >= 3:
        quality_points += 5
    # Organization (5 pts): Check if code contains at least 3 function definitions
    if code.count("def ") >= 3:
        quality_points += 5
    total_score += quality_points

    ## 3. JSON Path (10 Points):
    if "json_path" in code:
        total_score += 10

    ## 4. Sheet Creation (10 Points):
    if "Below_25" in code:
        total_score += 5
    if "Above_25" in code:
        total_score += 5

    #### Part 2: Uploaded HTML File Grading (15 Points Total) ####
    html_points = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read().lower()
            # Check for markers with color "blue"
            if "blue" in html_content:
                html_points += 5
            # Check for markers with color "red"
            if "red" in html_content:
                html_points += 10
    except Exception as e:
        print(f"Error reading HTML file: {e}")
    total_score += html_points

    #### Part 3: Uploaded Excel File Grading (35 Points Total) ####
    excel_points = 0
    try:
        uploaded_xl = pd.ExcelFile(excel_path)
        correct_xl = pd.ExcelFile(correct_excel_path)

        # Compare Sheet Names (15 Points)
        uploaded_sheets = set(map(str.lower, uploaded_xl.sheet_names))
        correct_sheets = set(map(str.lower, correct_xl.sheet_names))
        if uploaded_sheets == correct_sheets:
            excel_points += 15

        # Compare Column Names (10 Points)
        column_match = True
        for sheet in correct_xl.sheet_names:
            if sheet in uploaded_xl.sheet_names:
                correct_df = correct_xl.parse(sheet)
                uploaded_df = uploaded_xl.parse(sheet)
                correct_columns = set(map(str.lower, correct_df.columns))
                uploaded_columns = set(map(str.lower, uploaded_df.columns))
                if correct_columns != uploaded_columns:
                    column_match = False
        if column_match:
            excel_points += 10

        # Compare Data Equivalence (15 Points)
        data_match = True
        for sheet in correct_xl.sheet_names:
            if sheet in uploaded_xl.sheet_names:
                correct_df = correct_xl.parse(sheet).applymap(str.lower)
                uploaded_df = uploaded_xl.parse(sheet).applymap(str.lower)
                if not correct_df.equals(uploaded_df):
                    data_match = False
        if data_match:
            excel_points += 15

    except Exception as e:
        print(f"Error comparing Excel files: {e}")
    total_score += excel_points

    # Ensure the total score does not exceed 100
    return min(total_score, 100)
