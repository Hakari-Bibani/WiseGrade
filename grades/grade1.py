def grade_assignment(code):
    grade = 0

    # a. Library Imports (7 points: 5 for main libraries + 2 for pandas)
    required_imports = ["folium", "geopy", "geodesic", "pandas"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    if imported_libraries == 4:
        grade += 7
    elif imported_libraries == 3:
        grade += 5.25
    elif imported_libraries == 2:
        grade += 3.5
    elif imported_libraries == 1:
        grade += 1.75

    # b. Coordinate Handling (5 points)
    coordinates = ["36.325735, 43.928414", "36.393432, 44.586781", "36.660477, 43.840174"]
    correct_coordinates = sum(1 for coord in coordinates if coord in code)
    grade += correct_coordinates * (5 / 3)

    # c. Code Execution (10 points)
    try:
        local_context = {}
        exec(code, {}, local_context)
        grade += 10  # Full points if the code runs without errors
    except:
        pass  # No points if the code throws an error

    # d. Code Quality (10 points)
    code_quality_issues = 0
    if any(f" {char} =" in code or f" {char}=" in code for char in "abcdefghijklmnopqrstuvwxyz"):
        code_quality_issues += 1
    if "=" in code.replace(" = ", ""):
        code_quality_issues += 1
    if "#" not in code:
        code_quality_issues += 1
    if "\n\n" not in code:
        code_quality_issues += 1
    grade += max(0, 10 - code_quality_issues * 2.5)

    # 2. Map Visualization (40 points)
    if "folium.Map" in code:
        grade += 15
    marker_count = code.count("folium.Marker")
    grade += min(15, marker_count * 5)  # Each marker is worth 5 points, max 15 points
    if "PolyLine" in code:
        grade += 5
    if "popup=" in code:
        grade += 5

    # 3. Distance Calculations (30 points)
    if "geodesic" in code:
        grade += 10
        # Verify accuracy of distance calculations
        try:
            exec(code, {}, local_context)
            calculated_distances = [val for val in local_context.values() if isinstance(val, float)]
            # Add checks for expected distances (e.g., ~65.21 km, ~75.82 km, etc.)
            expected_distances = [65.21, 75.82, 33.84]  # Approx distances between points
            tolerance = 0.5  # Allowable error in km
            for expected in expected_distances:
                if any(abs(expected - calc) <= tolerance for calc in calculated_distances):
                    grade += 6.67  # Divide 20 points equally among 3 distances
        except:
            pass

    return round(grade)
