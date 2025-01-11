def calculate_grade(code):
    """Calculate the grade for the submitted code."""
    # Check for required libraries
    required_libraries = ["folium", "geopy", "geodesic"]
    library_score = 0
    for lib in required_libraries:
        if f"import {lib}" in code or f"from {lib}" in code:
            library_score += 1.67

    # Check for coordinate handling
    coordinates = [
        (36.325735, 43.928414),
        (36.393432, 44.586781),
        (36.660477, 43.840174),
    ]
    coordinate_score = 0
    for lat, lon in coordinates:
        if f"{lat}" in code and f"{lon}" in code:
            coordinate_score += 1.67

    # Check for distance calculations
    distance_score = 0
    if "geodesic(" in code:
        distance_score += 10

    # Check for map visualization
    map_score = 0
    if "folium.Map(" in code:
        map_score += 15
    if "folium.Marker(" in code:
        map_score += 15
    if "folium.PolyLine(" in code:
        map_score += 5
    if "popup=" in code:
        map_score += 5

    # Total grade
    total_grade = library_score + coordinate_score + distance_score + map_score
    return round(total_grade, 2)
