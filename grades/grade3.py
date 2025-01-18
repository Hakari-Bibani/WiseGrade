import os
import pandas as pd

def grade_assignment(code, html_path, excel_path, correct_excel_path):
    """
    Grades Assignment 3 based on the provided code, HTML file, and Excel file.
    Returns a numerical grade (0-100) with breakdowns.
    """
    total_score = 0
    grading_breakdown = {}

    #### Part 1: Code Grading (45 Points Total) ####

    ## 1. Library Imports (15 Points):
    lib_points = 0
    if any(lib in code for lib in ["gspread", "pygsheets", "google-api-python-client"]):
        lib_points += 6
    if any(lib in code for lib in ["pandas", "numpy"]):
        lib_points += 2
    if any(lib in code for lib in ["folium", "plotly", "geopandas", "matplotlib"]):
        lib_points += 7
    grading_breakdown["Library Imports"] = lib_points
    total_score += lib_points

    ## 2. Code Quality (20 Points):
    quality_points = 0
    descriptive_keywords = ["student_id", "code_input", "temperature", "longitude", "latitude"]
    if any(word in code for word in descriptive_keywords):
        quality_points += 5
    if " = " in code:
        quality_points += 5
    if "#" in code:
        quality_points += 5
    if "def " in code:
        quality_points += 5
    grading_breakdown["Code Quality"] = quality_points
    total_score += quality_points

    ## 3. JSON Path (5 Points):
    if "json_path" in code:
        grading_breakdown["JSON Path"] = 5
        total_score += 5
    else:
        grading_breakdown["JSON Path"] = 0

    ## 4. Sheet Creation (10 Points):
    sheet_points = 0
    if "Below_25" in code:
        sheet_points += 5
    if "Above_25" in code:
        sheet_points += 5
    grading_breakdown["Sheet Creation"] = sheet_points
    total_score += sheet_points

    #### Part 2: HTML File Grading (10 Points Total) ####
    html_points = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read().lower()
            if "blue" in html_content:
                html_points += 5
            if "red" in html_content:
                html_points += 5
    except Exception as e:
        print(f"Error reading HTML file: {e}")
    grading_breakdown["HTML File"] = html_points
    total_score += html_points

    #### Part 3: Excel File Grading (40 Points Total) ####
    excel_points = 0
    try:
        # Load the correct Excel file
        correct_xl = pd.ExcelFile(correct_excel_path)
        uploaded_xl = pd.ExcelFile(excel_path)

        # Compare Sheet Names (15 Points)
        correct_sheets = [sheet.lower() for sheet in correct_xl.sheet_names]
        uploaded_sheets = [sheet.lower() for sheet in uploaded_xl.sheet_names]
        if set(correct_sheets) == set(uploaded_sheets):
            excel_points += 15

        # Compare Column Names (10 Points)
        column_points = 0
        for sheet in correct_sheets:
            if sheet in uploaded_sheets:
                correct_df = correct_xl.parse(sheet)
                uploaded_df = uploaded_xl.parse(sheet)
                correct_cols = [col.lower() for col in correct_df.columns]
                uploaded_cols = [col.lower() for col in uploaded_df.columns]
                if correct_cols == uploaded_cols:
                    column_points += 5
        excel_points += column_points

        # Compare Data in "Above_25" Sheet (15 Points)
        if "above_25" in correct_sheets and "above_25" in uploaded_sheets:
            correct_above = correct_xl.parse("Above_25")
            uploaded_above = uploaded_xl.parse("Above_25")
            if abs(len(correct_above) - len(uploaded_above)) <= 3:
                excel_points += 15
    except Exception as e:
        print(f"Error processing Excel file: {e}")
    grading_breakdown["Excel File"] = excel_points
    total_score += excel_points

    # Ensure the total score does not exceed 100
    total_score = min(total_score, 100)
    return total_score, grading_breakdown
