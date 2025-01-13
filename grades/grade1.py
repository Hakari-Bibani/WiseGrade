def grade_assignment(code):
    grade = 0

    # a. Library Imports (5 points)
    required_imports = ["folium", "geopy", "geodesic", "pandas"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    if imported_libraries == 4:
        grade += 5
    elif imported_libraries == 3:
        grade += 3.75
    elif imported_libraries == 2:
        grade += 2.5
    elif imported_libraries == 1:
        grade += 1.25

    print(f"Library Import Score: {grade}/5")

    # b. Coordinate Handling (5 points)
    coordinates = ["36.325735, 43.928414", "36.393432, 44.586781", "36.660477, 43.840174"]
    correct_coordinates = sum(1 for coord in coordinates if coord in code)
    if correct_coordinates == 3:
        grade += 5
    elif correct_coordinates == 2:
        grade += 3.33
    elif correct_coordinates == 1:
        grade += 1.67

    print(f"Coordinate Handling Score: {grade - 5}/5")

    # c. Code Execution (10 points)
    try:
        local_context = {}
        exec(code, {}, local_context)
        grade += 10
        print("Code executed successfully.")
    except Exception as e:
        print(f"Execution Error: {e}")

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

    print(f"Code Quality Score: {grade - 15}/10")

    # 2. Map Visualization (40 points)
    if "folium.Map" in code:
        grade += 15

    marker_count = code.count("folium.Marker")
    grade += min(15, marker_count * 5)

    if "PolyLine" in code:
        grade += 5

    if "popup=" in code:
        grade += 5

    print(f"Map Visualization Score: {grade - 25}/40")

    # 3. Distance Calculations (30 points)
    if "geodesic" in code:
        grade += 10

        try:
            dataframe_object = next((obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None)
            if dataframe_object is not None:
                print("DataFrame found.")
                distance_col = next((col for col in dataframe_object.columns if "distance" in col.lower()), None)
                if distance_col:
                    print(f"Distance column detected: {distance_col}")
                    expected_distances = [59.57, 73.14, 37.98]
                    actual_distances = dataframe_object[distance_col].tolist()
                    correct_distances = 0
                    for expected, actual in zip(expected_distances, actual_distances):
                        if abs(expected - actual) <= 0.5:
                            correct_distances += 1
                    grade += correct_distances * (20 / len(expected_distances))
                    print(f"Correct distances: {correct_distances}")
                else:
                    print("Distance column not detected in DataFrame.")
            else:
                print("No DataFrame detected.")
        except Exception as e:
            print(f"Distance Calculation Validation Error: {e}")

    print(f"Final Distance Calculation Score: {grade - 65}/30")

    return round(grade)
