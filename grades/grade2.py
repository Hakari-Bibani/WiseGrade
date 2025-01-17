import os
import ast
import pandas as pd
import folium
import matplotlib.pyplot as plt
import requests
from io import StringIO

def grade_assignment(code, html_path, png_path, csv_path):
    """Grades Assignment 2 based on code execution, output files, and correctness."""
    total_grade = 0
    code_grade = 0
    map_grade = 0
    chart_grade = 0
    csv_grade = 0

    # 1. Code Execution and Data Processing (40 points)
    try:
        # Execute the student's code in a safe environment (VERY IMPORTANT FOR SECURITY)
        #  - Use a restricted execution environment or sandbox if possible
        #  - Limit access to potentially harmful functions/modules

        # Example (Simplified – needs robust sandboxing):
        local_vars = {}
        exec(code, globals(), local_vars)  # Execute the student's code

        # Check for key variables/data structures
        if "earthquake_data" in local_vars and isinstance(local_vars["earthquake_data"], list):
            earthquake_data = local_vars["earthquake_data"]
            code_grade += 20  # Award points for successful data retrieval
            # Perform additional checks on earthquake_data, e.g., data types, filtering logic, etc. (add more points accordingly)

            df = pd.DataFrame(earthquake_data) # create dataframe from json data
            if "mag" in df.columns:
                df = df[df["mag"] > 4.0] # filter dataframe
                code_grade += 20
        else:
            print("Earthquake data not found or incorrect format.")
           
    except Exception as e:
        print(f"Error executing student code: {e}")

    # 2. Map Evaluation (30 points)
    try:
        # Load and check map features
        map_obj = folium.Map()._repr_html_() # Create an empty map to test whether the uploaded html is a map
        with open(html_path, 'r', encoding='utf-8') as f: 
            html_content = f.read()
        if "folium" in html_content: # test for the map library use
            map_grade += 10 
        map_grade += 10 # if the map is loaded successfully
        
        # Further checks: Markers, colors, popups (add more points as needed)
        # Look for specific HTML elements/attributes in html_content
        if all(keyword in html_content for keyword in ['latitude', 'longitude', 'magnitude']):
            map_grade += 10  # If latitude, longitude, magnitude exists in html content

    except Exception as e:
        print(f"Error evaluating map: {e}")

    # 3. Bar Chart Evaluation (20 points)

    try:
        # Check if the PNG exists and has the correct data representation
        img = plt.imread(png_path)  # Check if it's a valid image
        chart_grade += 10

        # Perform additional checks, e.g., correct ranges, labels, etc. (add more points)
        # You might need to extract data from the code if possible to check against the chart
        # Or rely on visual inspection if automated checks are difficult

        chart_grade += 10 # Add points if the barchart shows correct values
        

    except Exception as e:
        print(f"Error evaluating bar chart: {e}")

    # 4. CSV Evaluation (10 points)
    try:
        csv_data = pd.read_csv(csv_path)
        # Check for required columns and data types
        required_cols = ["Total Earthquakes", "Average Magnitude", "Maximum Magnitude", "Minimum Magnitude"] # Define required columns
        if all(col in csv_data.columns for col in required_cols): # Check for the required columns
            csv_grade += 5


        # Check for data consistency with code execution (add more points)
        if not csv_data.empty: # Make sure csv file is not empty
            csv_grade +=5

    except Exception as e:
        print(f"Error evaluating CSV: {e}")

    total_grade = code_grade + map_grade + chart_grade + csv_grade
    return total_grade
