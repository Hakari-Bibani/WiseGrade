import re

def calculate_grade(code_input):
    grade = 0

    # Check library imports
    required_imports = ["import folium", "from geopy.distance import geodesic"]
    grade += sum(1.67 for imp in required_imports if imp in code_input)

    # Check for coordinates
    coordinates = ["36.325735, 43.928414", "36.393432, 44.586781", "36.660477, 43.840174"]
    grade += sum(1.67 for coord in coordinates if coord in code_input)

    # Check map generation and polyline
    if "folium.Map" in code_input:
        grade += 15
    if "folium.Marker" in code_input:
        grade += 15
    if "folium.PolyLine" in code_input:
        grade += 5

    # Check geodesic and distance calculations
    if "geodesic" in code_input:
        grade += 10

    # Calculate total grade
    return min(grade, 100)
