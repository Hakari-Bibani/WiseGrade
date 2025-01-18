import os
import pandas as pd


def grade_assignment(code, html_path, excel_path, correct_excel_path):
    """
    Grades Assignment 3 based on the provided code, HTML file, and Excel file.
    Returns a numerical grade (0-100).
    """

    total_score = 0

    #### Part 1: Code Grading (40 Points Total) ####

    ## 1. Library Imports (20 Points Total):
    lib_points = 0
    # Check for gspread, pygsheets, google-api-python-client (8 pts)
    if any(lib in code for lib in ["gspread", "pygsheets", "google-api-python-client"]):
        lib_points += 8
    # Check for pandas or numpy (4 pts)
    if any(lib in code for lib in ["pandas", "numpy"]):
        lib_points += 4
    # Check for folium, plotly, geopandas, matplotlib (8 pts)
    if any(lib in code for lib in ["folium", "plotly", "geopandas", "matplotlib"]):
        lib_points += 8
    total_score += lib_points

    ## 2. Code Quality (20 Points Total):
    quality_points = 0
    # Descriptive Variable Names (5 pts): check for common descriptive names
    descriptive_keywords = ["student_id", "code_input", "temperature", "longitude", "latitude"]
    if any(word in code for word in descriptive_keywords):
        quality_points += 5
    # Spacing (5 pts): check if code uses " = " instead of "="
    if " = " in code:
        quality_points += 5
    # Comments (5 pts): check for presence of comments (lines starting with #)
    if "#" in code:
        quality_points += 5
    # Organization (5 pts): check for function definitions
    if "def " in code:
        quality_points += 5
    total_score += quality_points

    ## 3. JSON Path (10 Points):
    if "json_path" in code:
        total_score += 10

    ## 4. Sheet Creation (10 Points):
    # Check for mentions of "Below_25" and "Above_25"
    if "Below_25" in code:
        total_score += 5
    if "Above_25" in code:
        total_score += 5

    #### Part 2: HTML File Grading (15 Points Total) ####
    html_points = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read().lower()
            # Check for markers with color "blue" (5 pts)
            if "blue" in html_content:
                html_points += 5
            # Check for markers with color "red" (10 pts)
            if "red" in html_content:
                html_points += 10
    except Exception as e:
        print(f"Error reading HTML file: {e}")
    total_score += html_points

    #### Part 3: Excel File Grading (45 Points Total) ####
    excel_points = 0
    try:
        # Load the uploaded Excel file
        uploaded_xl = pd.ExcelFile(excel_path)

        # Load the correct Excel file
        correct_xl = pd.ExcelFile(correct_excel_path)

        # Compare sheet names (15 pts)
        uploaded_sheets = [sheet.lower() for sheet in uploaded_xl.sheet_names]
        correct_sheets = [sheet.lower() for sheet in correct_xl.sheet_names]
        if uploaded_sheets == correct_sheets:
            excel_points += 15

        # Compare column names for each sheet (10 pts)
        for sheet in correct_xl.sheet_names:
            if sheet in uploaded_xl.sheet_names:
                uploaded_cols = [col.lower() for col in pd.read_excel(uploaded_xl, sheet).columns]
                correct_cols = [col.lower() for col in pd.read_excel(correct_xl, sheet).columns]
                if uploaded_cols == correct_cols:
                    excel_points += 10

        # Compare data equivalence for each sheet (15 pts)
        for sheet in correct_xl.sheet_names:
            if sheet in uploaded_xl.sheet_names:
                uploaded_df = pd.read_excel(uploaded_xl, sheet)
                correct_df = pd.read_excel(correct_xl, sheet)
                if uploaded_df.equals(correct_df):
                    excel_points += 15
    except Exception as e:
        print(f"Error processing Excel file: {e}")
    total_score += excel_points

    # Ensure the total score does not exceed 100
    return min(total_score, 100)
