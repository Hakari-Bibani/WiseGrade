import os
import pandas as pd

def grade_assignment(code, html_path, excel_path):
    """
    Grades Assignment 3 based on the pasted code and the two uploaded files.
    Returns a numerical grade (0-100) according to the following rubric:

    --- Pasted Code (60 Points Total) ---
    
    1. Library Imports (10 Points):
       - Contains one of: "gspread", "pygsheets", or "google-api-python-client" ==> 4 points
       - Contains one of: "pandas" or "numpy" ==> 2 points
       - Contains one of: "folium", "plotly", "geopandas", or "matplotlib" (with mapping extensions) ==> 4 points

    2. Code Quality (10 Points):
       - Descriptive Variable Names, Spacing, Comments, Organization: 5 points each (max 20 points)
         (For auto-grading purposes, this example uses simple heuristics. 
          Adjust the approach if you have a more advanced code quality checker.)
       * For this rubric, we award a total of 10 points based on whether at least two of these subcategories appear.
         (e.g., if two or more are clearly demonstrated, award full 10 points.)

    3. Presence of json_path (5 Points):
       - If the code includes the substring "json_path", award 5 points.

    4. Encapsulation (5 Points):
       - If the code defines at least three functions (indicating distinct stages, e.g., Stage 1, 2, and 3), award 5 points.

    5. Data Filtering in Code (10 Points Total):
       - If the code contains a filter for data below 25°C and saves it to a new sheet "Below_25" ==> 5 points.
       - If the code contains a filter for data above 25°C and saves it to a new sheet "Above_25" ==> 5 points.
       
    --- Uploaded Files (40 Points Total) ---

    6. HTML File of the Map (15 Points Total):
       - Check if the HTML file contains a substring indicating a marker 
         (e.g., "marker" or "circle-marker" or any marker type) ==> 5 points.
       - Check if the HTML file contains the color "green" ==> 5 points.
       - Check if the HTML file contains the color "red" ==> 5 points.

    7. Excel File (25 Points Total):
       A. Sheet Names (15 Points Total):
          - Contains a sheet named "Sheet1" ==> 5 points.
          - Contains a sheet named "Below_25" ==> 5 points.
          - Contains a sheet named "Above_25" ==> 5 points.
       B. Column Names (15 Points Total):
          For each sheet ("Sheet1", "Below_25", and "Above_25"), check that they contain
          columns for longitude, latitude, and temperature (or equivalent case-insensitive matches such as "temp").
          (Award 5 points per sheet, maximum 15 points.)
       C. Row Counts (10 Points Total):
          - "Below_25" must contain 264 rows (±3 rows tolerance) ==> 5 points.
          - "Above_25" must contain 237 rows (±3 rows tolerance) ==> 5 points.
          *(Note: Row count checks assume that the header row is not counted. Adjust if needed.)*

    The total maximum is 100 points.
    """

    total_score = 0

    ###############
    # PART I: PASTED CODE GRADING (60 Points Total)
    ###############

    # 1. Library Imports (10 Points)
    lib_points = 0
    # Check for one of these libraries: gspread / pygsheets / google-api-python-client
    if any(lib in code for lib in ["gspread", "pygsheets", "google-api-python-client"]):
        lib_points += 4
    # Check for pandas or numpy
    if any(lib in code for lib in ["pandas", "numpy"]):
        lib_points += 2
    # Check for one of these mapping libraries: folium, plotly, geopandas, or matplotlib (as mapping library)
    if any(lib in code for lib in ["folium", "plotly", "geopandas", "matplotlib"]):
        lib_points += 4
    total_score += lib_points
    # Debug:
    # print("Library Imports Points:", lib_points)

    # 2. Code Quality (10 Points)
    quality_points = 0
    # Use simple heuristics for four subcategories: descriptive names, spacing, comments, organization.
    quality_checks = 0
    # Descriptive Variable Names: look for common descriptive names (this is a heuristic)
    if any(word in code for word in ["student_id", "code_input", "temperature", "longitude", "latitude"]):
        quality_checks += 1
    # Spacing: check for " = " instance(s)
    if " = " in code:
        quality_checks += 1
    # Comments: check if there is any comment (look for "#")
    if "#" in code:
        quality_checks += 1
    # Organization: check if there are blank lines between functions or sections (look for "\n\n")
    if "\n\n" in code:
        quality_checks += 1
    # If at least 2 of these are clearly demonstrated, award full 10 points
    if quality_checks >= 2:
        quality_points = 10
    total_score += quality_points
    # Debug:
    # print("Code Quality Points:", quality_points)

    # 3. Presence of json_path (5 Points)
    json_path_points = 5 if "json_path" in code else 0
    total_score += json_path_points
    # Debug:
    # print("json_path Points:", json_path_points)

    # 4. Encapsulation of Functionality (5 Points)
    # Check if the code has at least three function definitions (i.e. "def " occurs at least 3 times)
    encapsulation_points = 5 if code.count("def ") >= 3 else 0
    total_score += encapsulation_points
    # Debug:
    # print("Encapsulation Points:", encapsulation_points)

    # 5. Data Filtering in Code (10 Points Total)
    filtering_points = 0
    if "Below_25" in code:
        filtering_points += 5
    if "Above_25" in code:
        filtering_points += 5
    total_score += filtering_points
    # Debug:
    # print("Data Filtering Points:", filtering_points)

    ###############
    # PART II: UPLOADED FILES GRADING (40 Points Total)
    ###############

    # 6. HTML File of the Map (15 Points)
    html_points = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read().lower()
            # Check for a marker (e.g., "marker", "circle-marker", etc.)
            if "marker" in html_content or "circle-marker" in html_content:
                html_points += 5
            # Check for green color
            if "green" in html_content:
                html_points += 5
            # Check for red color
            if "red" in html_content:
                html_points += 5
    except Exception as e:
        print(f"Error reading HTML file: {e}")
    total_score += html_points
    # Debug:
    # print("HTML Points:", html_points)

    # 7. Excel File (25 Points Total: 15 for Sheets + 15 for Columns + 10 for Row Counts)
    excel_points = 0
    try:
        xl = pd.ExcelFile(excel_path)
        sheet_names = xl.sheet_names

        # (A) Sheet Names (15 Points: 5 each)
        required_sheets = ["Sheet1", "Below_25", "Above_25"]
        for sheet in required_sheets:
            if sheet in sheet_names:
                excel_points += 5

        # (B) Column Names (15 Points Total: 5 points per sheet)
        # Expected columns: longitude, latitude, and temperature (or variations like temp)
        for sheet in required_sheets:
            if sheet in sheet_names:
                df_sheet = xl.parse(sheet)
                # Convert column names to lowercase strings
                cols = [str(col).lower() for col in df_sheet.columns]
                # Look for longitude
                has_long = any("long" in col for col in cols)
                # Look for latitude
                has_lat = any("lat" in col for col in cols)
                # Look for temperature (or temp)
                has_temp = any("temp" in col for col in cols)
                if has_long and has_lat and has_temp:
                    excel_points += 5

        # (C) Row Counts (10 Points Total)
        # For Below_25: expected 264 rows (tolerance ±3)
        if "Below_25" in sheet_names:
            df_below = xl.parse("Below_25")
            # Assuming header is not counted:
            if abs(len(df_below) - 264) <= 3:
                excel_points += 5
        # For Above_25: expected 237 rows (tolerance ±3)
        if "Above_25" in sheet_names:
            df_above = xl.parse("Above_25")
            if abs(len(df_above) - 237) <= 3:
                excel_points += 5

    except Exception as e:
        print(f"Error processing Excel file: {e}")

    total_score += excel_points
    # Debug:
    # print("Excel Points:", excel_points)

    # Final Score: ensure it does not exceed 100
    return min(total_score, 100)
