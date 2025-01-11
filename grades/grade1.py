import ast
import re

def calculate_grade(code):
    grade = 0

    # Check for required libraries
    if "import folium" in code and "from geopy.distance import geodesic" in code:
        grade += 5  # Library imports

    # Check for coordinate handling
    if re.search(r"point1\s*=\s*\([\d\.]+,\s*[\d\.]+\)", code):
        grade += 5  # Coordinate handling

    # Check for map generation
    if "folium.Map" in code:
        grade += 15  # Map generation

    # Check for markers
    if "folium.Marker" in code:
        grade += 15  # Markers

    # Check for polylines
    if "folium.PolyLine" in code:
        grade += 5  # Polylines

    # Check for popups
    if "popup=" in code:
        grade += 5  # Popups

    # Check for distance calculations
    if "geodesic" in code:
        grade += 10  # Geodesic implementation

    # Check for distance accuracy (basic check)
    if "kilometers" in code:
        grade += 20  # Distance accuracy

    return min(grade, 100)  # Ensure grade does not exceed 100
