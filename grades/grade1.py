def grade_assignment(code):
    grade = 0
    print("\n=== Grading Submission ===\n")

    # Library Imports (5 points)
    required_imports = ["folium", "geopy", "geodesic", "pandas"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    library_score = min(5, imported_libraries * 1.25)
    grade += library_score
    print(f"Library Imports: {library_score}/5")

    # Coordinates (5 points)
    coordinates = ["36.325735, 43.928414", "36.393432, 44.586781", "36.660477, 43.840174"]
    correct_coordinates = sum(1 for coord in coordinates if coord in code)
    coordinate_score = min(5, correct_coordinates * (5 / 3))
    grade += coordinate_score
    print(f"Coordinate Handling: {coordinate_score}/5")

    # Code Execution (10 points)
    try:
        local_context = {}
        exec(code, {}, local_context)
        execution_score = 10
        grade += execution_score
        print("Code Execution: Success (10/10)")
    except Exception as e:
        execution_score = 0
        print(f"Code Execution: Error ({e}) (0/10)")

    # Code Quality (10 points)
    code_quality_issues = 0
    if any(f" {char} =" in code or f" {char}=" in code for char in "abcdefghijklmnopqrstuvwxyz"):
        code_quality_issues += 1
    if "=" in code.replace(" = ", ""):
        code_quality_issues += 1
    if "#" not in code:
        code_quality_issues += 1
    if "\n\n" not in code:
        code_quality_issues += 1
    quality_score = max(0, 10 - code_quality_issues * 2.5)
    grade += quality_score
    print(f"Code Quality: {quality_score}/10")

    # Map Visualization (40 points)
    map_score = 0
    if "folium.Map" in code:
        map_score += 15
        print("Map Generation: Detected (15/15)")
    else:
        print("Map Generation: Not Detected (0/15)")

    marker_count = code.count("folium.Marker")
    marker_score = min(15, marker_count * 5)
    map_score += marker_score
    print(f"Markers: {marker_score}/15")

    if "PolyLine" in code:
        map_score += 5
        print("Polylines: Detected (5/5)")
    else:
        print("Polylines: Not Detected (0/5)")

    if "popup=" in code:
        map_score += 5
        print("Popups: Detected (5/5)")
    else:
        print("Popups: Not Detected (0/5)")

    grade += map_score
    print(f"Map Visualization: {map_score}/40")

    # Distance Calculations (30 points)
    distance_score = 0
    if "geodesic" in code:
        distance_score += 10
        print("Geodesic Function: Detected (10/10)")
        try:
            dataframe_object = next((obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None)
            if dataframe_object is not None:
                print("DataFrame Detected")
                distance_col = next((col for col in dataframe_object.columns if "distance" in col.lower()), None)
                if distance_col:
                    print(f"Distance Column Found: {distance_col}")
                    expected_distances = [59.57, 73.14, 37.98]
                    actual_distances = dataframe_object[distance_col].tolist()
                    print(f"Expected Distances: {expected_distances}")
                    print(f"Actual Distances: {actual_distances}")

                    correct_distances = 0
                    tolerance = 0.5
                    for expected, actual in zip(expected_distances, actual_distances):
                        if abs(expected - actual) <= tolerance:
                            correct_distances += 1

                    distance_score += correct_distances * (20 / len(expected_distances))
                    print(f"Correct Distances: {correct_distances}, Distance Score: {distance_score}")
                else:
                    print("Distance Column Missing")
            else:
                print("No DataFrame Detected")
        except Exception as e:
            print(f"Distance Validation Error: {e}")
    else:
        print("Geodesic Function: Not Detected (0/10)")

    grade += distance_score
    print(f"Distance Calculations: {distance_score}/30")

    print(f"\n=== Final Grade: {round(grade)}/100 ===\n")
    return round(grade)
