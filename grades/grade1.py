def grade_assignment(code):
    grade = 0

    # a. Library Imports (5 points)
    required_imports = ["folium", "geopy", "geodesic"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    if imported_libraries == 3:
        grade += 5
    elif imported_libraries == 2:
        grade += 3.33
    elif imported_libraries == 1:
        grade += 1.67

    # b. Coordinate Handling (5 points)
    coordinates = ["36.325735, 43.928414", "36.393432, 44.586781", "36.660477, 43.840174"]
    correct_coordinates = sum(1 for coord in coordinates if coord in code)
    if correct_coordinates == 3:
        grade += 5
    elif correct_coordinates == 2:
        grade += 3.33
    elif correct_coordinates == 1:
        grade += 1.67

    # c. Code Execution (10 points)
    try:
        exec(code)
        grade += 10  # Full points if the code runs without errors
    except:
        pass  # No points if the code throws an error

    # d. Code Quality (10 points)
    code_quality_issues = 0
    # Check for single-letter variables
    if any(f" {char} =" in code or f" {char}=" in code for char in "abcdefghijklmnopqrstuvwxyz"):
        code_quality_issues += 1
    # Check for improper spacing (e.g., no space after =)
    if "=" in code.replace(" = ", ""):
        code_quality_issues += 1
    # Check for absence of comments
    if "#" not in code:
        code_quality_issues += 1
    # Check for lack of code organization (no blank lines for separation)
    if "\n\n" not in code:
        code_quality_issues += 1
    # Deduct points based on issues
    if code_quality_issues == 0:
        grade += 10
    elif code_quality_issues == 1:
        grade += 8
    elif code_quality_issues == 2:
        grade += 6
    elif code_quality_issues == 3:
        grade += 4
    elif code_quality_issues == 4:
        grade += 2

    # 2. Map Visualization (40 points)
    # a. Map Generation (15 points)
    if "folium.Map" in code:
        grade += 15

    # b. Markers (15 points)
    marker_count = code.count("folium.Marker")
    if marker_count >= 3:
        grade += 15
    elif marker_count == 2:
        grade += 10
    elif marker_count == 1:
        grade += 5

    # c. Polylines (5 points)
    if "PolyLine" in code:
        grade += 5

    # d. Popups (5 points)
    if "popup=" in code:
        grade += 5

    # 3. Distance Calculations (30 points)
    # a. Geodesic Implementation (10 points)
    if "geodesic" in code:
        grade += 10

    # b. Distance Accuracy (20 points)
    # Assuming the code calculates distances and stores them in variables or outputs them
    # This part requires manual verification or additional logic to check accuracy
    # For now, we assume full points if geodesic is used
    if "geodesic" in code:
        grade += 20

    return round(grade)
