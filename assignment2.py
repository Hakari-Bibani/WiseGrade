import ast
import re
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import numpy as np

def grade_assignment(code, html_path, png_path, csv_path):
    total_points = 100
    grade = 0

    # 1. Library Imports (20 points)
    points = 20
    required_imports = ['requests', 'folium', 'pandas']
    try:
        tree = ast.parse(code)
        imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
        if all(import_ in imports for import_ in required_imports):
            grade += points
        else:
            print("Missing required library imports.")
    except Exception as e:
        print(f"Error evaluating library imports: {e}")
        points = 0

    # 2. Code Quality (10 points)
    points = 10
    try:
        variables = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', code)
        if all(len(variable) > 2 for variable in variables):
            grade += points
        else:
            print("Variable names are not descriptive.")
    except Exception as e:
        print(f"Error evaluating code quality: {e}")
        points = 0

    # 3. Fetching Data from API (10 points)
    points = 10
    try:
        if 'requests.get' in code and 'response.status_code' in code:
            grade += points
        else:
            print("API request or error handling is incorrect.")
    except Exception as e:
        print(f"Error evaluating API request: {e}")
        points = 0

    # 4. Filtering Earthquakes (10 points)
    points = 10
    try:
        if 'df.query' in code or ('df[' in code and '> 4.0' in code):
            grade += points
        else:
            print("Earthquake filtering is incorrect.")
    except Exception as e:
        print(f"Error evaluating earthquake filtering: {e}")
        points = 0

    # 5. Map Visualization (20 points)
    points = 20
    try:
        with open(html_path, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            markers = soup.find_all('div', {'class': 'leaflet-marker-icon'})
            if len(markers) > 0:
                grade += points
            else:
                print("Map markers are missing.")
    except Exception as e:
        print(f"Error evaluating map visualization: {e}")
        points = 0

    # 6. Bar Chart (15 points)
    points = 15
    try:
        img = plt.imread(png_path)
        if img.shape[2] == 4:  # RGBA (with alpha channel)
            grade += points
        else:
            print("Bar chart is incorrect.")
    except Exception as e:
        print(f"Error evaluating bar chart: {e}")
        points = 0

    # 7. Text Summary (15 points)
    points = 15
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            metrics = [row['Metric'] for row in data]
            values = [float(row['Value']) for row in data]
            if (np.isclose(values[0], 218.0, atol=1) and
                np.isclose(values[1], 4.63, atol=0.3) and
                np.isclose(values[2], 7.1, atol=0.2) and
                np.isclose(values[3], 4.1, atol=0.2) and
                np.isclose(values[4], 75.0, atol=1) and
                np.isclose(values[5], 106.0, atol=0.3) and
                np.isclose(values[6], 37.0, atol=1)):
                grade += points
            else:
                print("Text summary is incorrect.")
    except Exception as e:
        print(f"Error evaluating text summary: {e}")
        points = 0

    return grade
