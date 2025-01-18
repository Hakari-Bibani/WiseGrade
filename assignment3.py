import os
import pandas as pd
import difflib

def grade_assignment(code, html_path, excel_path):
    """
    Grades Assignment 3 based on the provided code, HTML file, and Excel file.
    Returns a numerical grade (0-100).
    """
    total_score = 0

    #### Part 1: Code Grading (45 Points Total) ####

    ## 1. Library Imports (20 Points Total):
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

    ## 2. Code Quality (20 Points Total):
    quality_points = 0
    # Descriptive Variable Names, Spacing, Comments, Organization (5 pts each)
    # Simple heuristic checks (improve as needed)
    if any(keyword in code for keyword in ["student_id", "temperature", "longitude", "latitude"]):
        quality_points += 5  # Descriptive Variable Names
    if " = " in code:
        quality_points += 5  # Spacing
    if "#" in code:
        quality_points += 5  # Comments
    if code.count("def ") >= 3:
        quality_points += 5  # Organization
    total_score += quality_points

    ## 3. JSON Path (10 Points):
    if "json_path" in code:
        total_score += 10

    ## 4. Creating Sheets (10 Points Total):
    # Award 5 points each for creating sheets named "Below_25" and "Above_25"
    if "Below_25" in code:
        total_score += 5
    if "Above_25" in code:
        total_score += 5

    #### Part 2: HTML File Grading (15 Points Total) ####
    html_points = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read().lower()
            # Check for blue and red points
            if "blue" in html_content:
                html_points += 5
            if "red" in html_content:
                html_points += 10
    except Exception as e:
        print(f"Error reading HTML file: {e}")
    total_score += html_points

    #### Part 3: Excel File Grading (40 Points Total) ####
    excel_points = 0
    correct_excel_path = os.path.join("grades", "correct_data.xlsx")  # Path to correct Excel file

    try:
        # Load the uploaded and correct Excel files
        uploaded_xl = pd.ExcelFile(excel_path)
        correct_xl = pd.ExcelFile(correct_excel_path)

        # Compare sheet names (15 points)
        uploaded_sheets = [sheet.lower() for sheet in uploaded_xl.sheet_names]
        correct_sheets = [sheet.lower() for sheet in correct_xl.sheet_names]
        if sorted(uploaded_sheets) == sorted(correct_sheets):
            excel_points += 15

        # Compare column names for each sheet (10 points)
        for sheet in correct_sheets:
            if sheet in uploaded_sheets:
                uploaded_df = uploaded_xl.parse(sheet)
                correct_df = correct_xl.parse(sheet)
                uploaded_cols = [col.lower() for col in uploaded_df.columns]
                correct_cols = [col.lower() for col in correct_df.columns]
                if sorted(uploaded_cols) == sorted(correct_cols):
                    excel_points += 10
                    break

        # Compare data for each sheet (15 points)
        for sheet in correct_sheets:
            if sheet in uploaded_sheets:
                uploaded_df = uploaded_xl.parse(sheet).fillna("")
                correct_df = correct_xl.parse(sheet).fillna("")
                if uploaded_df.equals(correct_df):
                    excel_points += 15
                    break

    except Exception as e:
        print(f"Error comparing Excel files: {e}")

    total_score += excel_points

    # Ensure the total score does not exceed 100
    return min(total_score, 100)
