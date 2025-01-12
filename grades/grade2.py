# grades/grade2.py
import ast
import re
import pandas as pd
import folium
import matplotlib.pyplot as plt

def grade_assignment(code_input):
    """
    Grade the student's code for Assignment 2 based on the provided grading criteria.
    """
    total_score = 100  # Start with full marks and deduct for errors

    try:
        # Parse the student's code into an abstract syntax tree (AST)
        tree = ast.parse(code_input)

        # Initialize deduction counters
        deductions = {
            "library_imports": 0,
            "code_quality": 0,
            "api_fetching": 0,
            "filtering": 0,
            "map_visualization": 0,
            "bar_chart": 0,
            "text_summary": 0,
            "execution": 0,
        }

        # 1. Library Imports (10 Points)
        required_libraries = {"folium", "matplotlib", "requests", "pandas"}
        imported_libraries = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_libraries.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imported_libraries.add(node.module)

        # Check for missing or unnecessary libraries
        missing_libraries = required_libraries - imported_libraries
        unnecessary_libraries = imported_libraries - required_libraries

        if missing_libraries:
            deductions["library_imports"] += 2 * len(missing_libraries)
        if unnecessary_libraries:
            deductions["library_imports"] += 1 * len(unnecessary_libraries)

        # 2. Code Quality (20 Points)
        # Check variable naming, spacing, comments, and organization
        code_lines = code_input.split("\n")
        single_letter_vars = re.findall(r"\b[a-zA-Z]\b", code_input)
        improper_spacing = re.findall(r"[=><][^ ]", code_input)
        missing_comments = sum(1 for line in code_lines if not line.strip().startswith("#") and not line.strip() == "")
        poor_organization = sum(1 for line in code_lines if line.strip() == "")

        # Deduct for code quality issues
        if single_letter_vars:
            deductions["code_quality"] += 1 * len(single_letter_vars)
        if improper_spacing:
            deductions["code_quality"] += 1 * len(improper_spacing)
        if missing_comments > 5:  # Allow up to 5 missing comments
            deductions["code_quality"] += 1 * (missing_comments - 5)
        if poor_organization < 5:  # Expect at least 5 blank lines for organization
            deductions["code_quality"] += 1 * (5 - poor_organization)

        # 3. Fetching Data from the API (10 Points)
        if "requests.get(" not in code_input and "urllib.request.urlopen(" not in code_input:
            deductions["api_fetching"] += 3  # Missing API call
        if "response.status_code" not in code_input:
            deductions["api_fetching"] += 4  # Missing error handling

        # 4. Filtering Earthquakes (10 Points)
        if "magnitude > 4.0" not in code_input:
            deductions["filtering"] += 5  # Incorrect filtering logic
        if "latitude" not in code_input or "longitude" not in code_input or "time" not in code_input:
            deductions["filtering"] += 2  # Missing required data fields

        # 5. Map Visualization (20 Points)
        if "folium.Map(" not in code_input:
            deductions["map_visualization"] += 5  # Map not generated
        if "folium.Icon(color=" not in code_input:
            deductions["map_visualization"] += 3  # Missing color coding
        if "folium.Popup(" not in code_input:
            deductions["map_visualization"] += 2  # Missing popups

        # 6. Bar Chart (15 Points)
        if "plt.bar(" not in code_input:
            deductions["bar_chart"] += 5  # Bar chart not generated
        if "4.0-4.5" not in code_input or "4.5-5.0" not in code_input or "5.0+" not in code_input:
            deductions["bar_chart"] += 3  # Incorrect magnitude ranges
        if "plt.xlabel(" not in code_input or "plt.ylabel(" not in code_input:
            deductions["bar_chart"] += 1  # Missing labels

        # 7. Text Summary (15 Points)
        if "total_earthquakes" not in code_input:
            deductions["text_summary"] += 3  # Missing total earthquakes
        if "average_magnitude" not in code_input or "max_magnitude" not in code_input or "min_magnitude" not in code_input:
            deductions["text_summary"] += 3  # Missing magnitude metrics
        if "to_csv(" not in code_input:
            deductions["text_summary"] += 5  # Summary not saved as CSV

        # 8. Overall Execution (10 Points)
        # Deduct if the script crashes or produces incorrect outputs
        # This is handled by the try-except block in the main script

        # Calculate the final score
        total_deductions = sum(deductions.values())
        final_score = max(0, total_score - total_deductions)

        return final_score

    except Exception as e:
        # Deduct 10 points for execution errors
        return max(0, total_score - 10)
