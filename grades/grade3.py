import os
import pandas as pd


def grade_assignment(code, html_path, excel_path, correct_excel_path):
    """
    Grades Assignment 3 based on the provided code, HTML file, and Excel file.
    Returns a numerical grade (0-100).
    """

    total_score = 0

    #### Part 1: Code Grading (50 Points Total) ####

    ## 1. Library Imports (15 Points):
    lib_points = 0
    # Check for gspread/pygsheets/google-api-python-client (6 pts)
    if any(lib in code for lib in ["gspread", "pygsheets", "google-api-python-client"]):
        lib_points += 6
    # Check for pandas/numpy (2 pts)
    if any(lib in code for lib in ["pandas", "numpy"]):
        lib_points += 2
    # Check for folium/plotly/geopandas/matplotlib (7 pts)
    if any(lib in code for lib in ["folium", "plotly", "geopandas", "matplotlib"]):
        lib_points += 7
    total_score += lib_points

    ## 2. Code Quality (20 Points):
    quality_points = 0
    # Descriptive Variable Names (5 pts)
    descriptive_keywords = ["student_id", "code_input", "temperature", "longitude", "latitude"]
    if any(word in code for word in descriptive_keywords):
        quality_points += 5
    # Spacing (5 pts): Simple heuristic, checks for " = " spacing
    if " = " in code:
        quality_points += 5
    # Comments (5 pts): Checks if the code contains at least one comment
    if "#" in code:
        quality_points += 5
    # Organization (5 pts): Checks if the code defines at least 3 functions
    if code.count("def ") >= 3:
        quality_points += 5
    total_score += quality_points

    ## 3. JSON Path (5 Points):
    if "json_path" in code:
        total_score += 5

    ## 4. Sheet Creation (10 Points):
    # 5 points each for "Below_25" and "Above_25" references in the code
    if "Below_25" in code:
        total_score += 5
    if "Above_25" in code:
        total_score += 5

    #### Part 2: HTML File Grading (10 Points Total) ####
    html_points = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read().lower()
            # Check for blue marker (5 pts)
            if "blue" in html_content:
                html_points += 5
            # Check for red marker (5 pts)
            if "red" in html_content:
                html_points += 5
    except Exception as e:
        print(f"Error reading HTML file: {e}")
    total_score += html_points

    #### Part 3: Excel File Grading (40 Points Total) ####
    excel_points = 0
    try:
        # Load the uploaded Excel file and the correct reference Excel file
        uploaded_xl = pd.ExcelFile(excel_path)
        correct_xl = pd.ExcelFile(correct_excel_path)

        # Check Sheet Names (15 Points)
        uploaded_sheets = [sheet.lower() for sheet in uploaded_xl.sheet_names]
        correct_sheets = [sheet.lower() for sheet in correct_xl.sheet_names]
        if set(correct_sheets) == set(uploaded_sheets):
            excel_points += 15

        # Check Column Names (10 Points)
        for sheet in correct_sheets:
            if sheet in uploaded_sheets:
                uploaded_cols = [col.lower() for col in uploaded_xl.parse(sheet).columns]
                correct_cols = [col.lower() for col in correct_xl.parse(sheet).columns]
                if set(correct_cols) == set(uploaded_cols):
                    excel_points += 10 / len(correct_sheets)  # Distribute points across all sheets

        # Check Data Equivalence (15 Points)
        for sheet in correct_sheets:
            if sheet in uploaded_sheets:
                uploaded_data = uploaded_xl.parse(sheet)
                correct_data = correct_xl.parse(sheet)
                # Compare DataFrames (ignoring index and column order)
                if uploaded_data.equals(correct_data):
                    excel_points += 15 / len(correct_sheets)  # Distribute points across all sheets

    except Exception as e:
        print(f"Error processing Excel file: {e}")
    total_score += excel_points

    # Ensure the total score does not exceed 100
    return min(total_score, 100)
