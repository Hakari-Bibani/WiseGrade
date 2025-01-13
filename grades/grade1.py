def grade_assignment(code): 
    grade = 0

    # Debugging logs
    print("Starting grading process...")

    # a. Library Imports (5 points)
    required_imports = ["folium", "geopy", "geodesic", "pandas"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    print(f"Imported libraries count: {imported_libraries}")
    if imported_libraries == 4:
        grade += 5
    elif imported_libraries == 3:
        grade += 3.75
    elif imported_libraries == 2:
        grade += 2.5
    elif imported_libraries == 1:
        grade += 1.25

    # b. Coordinate Handling (5 points)
    coordinates = ["36.325735, 43.928414", "36.393432, 44.586781", "36.660477, 43.840174"]
    correct_coordinates = sum(1 for coord in coordinates if coord in code)
    print(f"Correct coordinates count: {correct_coordinates}")
    if correct_coordinates == 3:
        grade += 5
    elif correct_coordinates == 2:
        grade += 3.33
    elif correct_coordinates == 1:
        grade += 1.67

    # c. Code Execution (10 points)
    try:
        local_context = {}
        exec(code, {}, local_context)
        print("Code executed successfully.")
        print("Local Context Variables:", local_context.keys())
        grade += 10  # Full points if the code runs without errors
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

    # 2. Map Visualization (40 points)
    if "folium.Map" in code:
        grade += 15
    print(f"Grade after map generation: {grade}")

    marker_count = code.count("folium.Marker")
    grade += min(15, marker_count * 5)  # Each marker is worth 5 points, max 15 points
    print(f"Grade after markers: {grade}")

    if "PolyLine" in code:
        grade += 5

    if "popup=" in code:
        grade += 5

    print(f"Grade after polylines and popups: {grade}")

    # 3. Distance Calculations (30 points)
    if "geodesic" in code:
        grade += 10  # Full points for geodesic implementation
        print("Geodesic function detected.")

        # Verify accuracy of distance calculations
        try:
            exec(code, {}, local_context)
            dataframe_object = next((obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None)
            if dataframe_object is not None:
                print("DataFrame detected in local context.")
                print(dataframe_object)

                # Validate distances
                expected_distances = [59.57, 73.14, 37.98]  # Expected distances
                tolerance = 0.5  # Allowable error in km
                actual_distances = dataframe_object["Distance (km)"].tolist()
                print(f"Actual distances: {actual_distances}")

                for expected, actual in zip(expected_distances, actual_distances):
                    if abs(expected - actual) <= tolerance:
                        grade += 6.67  # Divide 20 points equally among 3 distances
            else:
                print("No DataFrame with distances found.")
        except Exception as e:
            print(f"Distance Verification Error: {e}")

    print(f"Final grade: {round(grade)}")
    return round(grade)
