def calculate_grade(user_code):
    """
    Calculate the grade for Assignment 1 based on the submitted code.
    """
    grade = 0

    # Check for required libraries
    required_libraries = ["folium", "geopy", "geodesic"]
    for lib in required_libraries:
        if lib in user_code:
            grade += 1.67

    # Check for distance calculations
    if "geodesic" in user_code and "kilometers" in user_code:
        grade += 20

    # Check for map plotting
    if "folium.Map" in user_code and "folium.Marker" in user_code:
        grade += 15

    # Check for polylines
    if "folium.PolyLine" in user_code:
        grade += 5

    # Check for popups
    if "popup" in user_code:
        grade += 5

    # Ensure grade does not exceed 100
    return min(grade, 100)
