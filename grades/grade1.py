def grade_assignment(code):
    grade = 0

    # Check library imports
    required_imports = ["folium", "geopy", "geodesic"]
    grade += sum(1.67 for lib in required_imports if lib in code)  # Up to 5 points

    # Check coordinate handling
    coordinates = ["36.325735, 43.928414", "36.393432, 44.586781", "36.660477, 43.840174"]
    grade += sum(1.67 for coord in coordinates if coord in code)  # Up to 5 points

    # Check code execution
    try:
        exec(code)
        grade += 10  # If code executes without errors
    except:
        pass

    # Check map visualization and distance calculations
    if "folium.Map" in code: grade += 15
    if ".add_to" in code and "Marker" in code: grade += 15
    if "PolyLine" in code: grade += 5
    if "geodesic" in code: grade += 10

    # Check distance accuracy
    if "36.325735" in code and "43.928414" in code: grade += 6.67  # Adjust logic as needed

    return round(grade)
