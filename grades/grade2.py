import os
import requests
import pandas as pd
import folium
import matplotlib.pyplot as plt
from io import StringIO

def grade_code(code):
    # Check for required libraries
    libraries = ['folium', 'matplotlib', 'requests', 'pandas']
    for lib in libraries:
        if lib not in code:
            return 0, "Missing required library: " + lib

    # Check for API call
    api_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    if api_url not in code:
        return 0, "API call not found"

    # Check for data filtering
    if "magnitude > 4.0" not in code:
        return 0, "Data filtering not implemented"

    # Check for map creation
    if "folium.Map" not in code:
        return 0, "Map not created"

    # Check for bar chart creation
    if "plt.bar" not in code or "seaborn.barplot" not in code:
        return 0, "Bar chart not created"

    # Check for CSV summary
    if "pd.DataFrame.to_csv" not in code:
        return 0, "CSV summary not generated"

    return 10, "Code meets requirements"


def grade_map(html_path):
    try:
        # Check for map markers
        with open(html_path, 'r') as f:
            html = f.read()
            if "folium.Marker" not in html:
                return 0, "Map markers not found"

        # Check for popup information
        if "folium.Popup" not in html:
            return 0, "Popup information not found"

        return 20, "Map meets requirements"
    except Exception as e:
        return 0, str(e)


def grade_bar_chart(png_path):
    try:
        # Check for bar chart
        img = plt.imread(png_path)
        if img.shape[2] != 4:  # RGBA
            return 0, "Bar chart not found"

        return 20, "Bar chart meets requirements"
    except Exception as e:
        return 0, str(e)


def grade_csv_summary(csv_path):
    try:
        # Check for CSV summary
        df = pd.read_csv(csv_path)
        required_columns = ["Total Earthquakes", "Average Magnitude", "Max Magnitude", "Min Magnitude"]
        if not all(col in df.columns for col in required_columns):
            return 0, "Required columns not found"

        return 20, "CSV summary meets requirements"
    except Exception as e:
        return 0, str(e)


def grade_assignment(code, html_path, png_path, csv_path):
    code_grade, code_feedback = grade_code(code)
    map_grade, map_feedback = grade_map(html_path)
    bar_chart_grade, bar_chart_feedback = grade_bar_chart(png_path)
    csv_grade, csv_feedback = grade_csv_summary(csv_path)

    total_grade = code_grade + map_grade + bar_chart_grade + csv_grade
    feedback = "\n".join([code_feedback, map_feedback, bar_chart_feedback, csv_feedback])

    return total_grade, feedback


if __name__ == "__main__":
    # Example usage
    code = open("example_code.py", "r").read()
    html_path = "example_map.html"
    png_path = "example_bar_chart.png"
    csv_path = "example_summary.csv"

    grade, feedback = grade_assignment(code, html_path, png_path, csv_path)
    print(f"Grade: {grade}/80")
    print(feedback)
