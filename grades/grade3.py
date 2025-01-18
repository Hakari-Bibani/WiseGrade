import os
import pandas as pd

def grade_assignment(code, html_path, excel_path):
    """
    Grades Assignment 3 based on the provided code, HTML file, and Excel file.
    Returns a numerical grade (0-100).
    """

    total_score = 0

    #### Part 1: Code Grading (45 Points Total) ####

    ## 1. Library Imports (10 Points):
    lib_points = 0
    # Check for gspread/pygsheets/google-api-python-client (4 pts)
    if any(lib in code for lib in ["gspread", "pygsheets", "google-api-python-client"]):
        lib_points += 4
    # Check for pandas/numpy (2 pts)
    if any(lib in code for lib in ["pandas", "numpy"]):
        lib_points += 2
    # Check for folium/plotly/geopandas/matplotlib (4 pts)
    if any(lib in code for lib in ["folium", "plotly", "geopandas", "matplotlib"]):
        lib_points += 4
    total_score += lib_points

    ## 2. Code Quality (10 Points):
    quality_points = 0
    # Descriptive Variable Names (heuristic): check for presence of some common descriptive names
    descriptive_keywords = ["student_id", "code_input", "temperature", "longitude", "latitude"]
    if any(word in code for word in descriptive_keywords):
        quality_points += 5
    # Spacing: check if code uses " = " instead of "=" (heuristic)
    if " = " in code:
        quality_points += 5
    total_score += quality_points

    ## 3. Using JSON API (10 Points):
    json_points = 0
    if "json" in code.lower() and "requests" in code.lower():
        json_points = 10
    total_score += json_points

    ## 4. Encapsulation (5 Points):
    # Check if the code defines at least 3 functions
    if code.count("def ") >= 3:
        total_score += 5

    ## 5. Data Filtering (Below/Above 25°C) (5 Points Each):
    if "Below_25" in code:
        total_score += 5
    if "Above_25" in code:
        total_score += 5

    #### Part 2: HTML File Grading (15 Points Total) ####
    html_points = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read().lower()
            # Check for a marker substring
            if "marker" in html_content:
                html_points += 5
            # Check for green and red colors
            if "green" in html_content:
                html_points += 5
            if "red" in html_content:
                html_points += 5
    except Exception as e:
        print(f"Error reading HTML file: {e}")
    total_score += html_points

    #### Part 3: Excel File Grading (40 Points Total) ####
    excel_points = 0
    try:
        # Read all sheet names
        xl = pd.ExcelFile(excel_path)
        sheet_names = xl.sheet_names

        # Check Sheet Names: "Sheet1", "Below_25", "Above_25" (5 pts each)
        required_sheets = ["Sheet1", "Below_25", "Above_25"]
        for sheet in required_sheets:
            if sheet in sheet_names:
                excel_points += 5

        # Validate Column Names for each required sheet (5 pts per sheet)
        # Expect columns: longitude, latitude, and temperature (or 'temp') – match case-insensitively.
        for sheet in required_sheets:
            if sheet in sheet_names:
                df = xl.parse(sheet)
                cols = [col.lower() for col in df.columns.astype(str)]
                if any("long" in col for col in cols) and any("lat" in col for col in cols) and (any("temp" in col for col in cols) or any("temperature" in col for col in cols)):
                    excel_points += 5

        # Validate Row Counts in "Below_25" and "Above_25"
        # Allow tolerance ±3 rows
        if "Below_25" in sheet_names:
            df_below = xl.parse("Below_25")
            expected = 264
            if abs(len(df_below) - expected) <= 3:
                excel_points += 5
        if "Above_25" in sheet_names:
            df_above = xl.parse("Above_25")
            expected = 237
            if abs(len(df_above) - expected) <= 3:
                excel_points += 5
    except Exception as e:
        print(f"Error processing Excel file: {e}")
    total_score += excel_points

    # Ensure the total score does not exceed 100
    return min(total_score, 100)
