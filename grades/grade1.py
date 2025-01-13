def grade_assignment(code):
    grade = 0

    # Library Imports (5 points)
    required_imports = ["folium", "geopy", "geodesic", "pandas"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    grade += min(5, imported_libraries * 1.25)

    # Coordinates (5 points)
    coordinates = ["36.325735, 43.928414", "36.393432, 44.586781", "36.660477, 43.840174"]
    correct_coordinates = sum(1 for coord in coordinates if coord in code)
    grade += min(5, correct_coordinates * (5 / 3))

    # Code Execution (10 points)
    try:
        local_context = {}
        exec(code, {}, local_context)
        grade += 10
    except Exception as e:
        print(f"Execution Error: {e}")

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
    grade += max(0, 10 - code_quality_issues * 2.5)

    # Map Visualization (40 points)
    if "folium.Map" in code:
        grade += 15

    marker_count = code.count("folium.Marker")
    grade += min(15, marker_count * 5)

    if "PolyLine" in code:
        grade += 5

    if "popup=" in code:
        grade += 5

    # Distance Calculations (30 points)
    if "geodesic" in code:
        grade += 10
        try:
            dataframe_object = next((obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None)
            if dataframe_object is not None:
                distance_col = next((col for col in dataframe_object.columns if "distance" in col.lower()), None)
                if distance_col:
                    expected_distances = [59.57, 73.14, 37.98]
                    tolerance = 0.5
                    actual_distances = dataframe_object[distance_col].tolist()
                    correct_distances = sum(
                        1 for expected, actual in zip(expected_distances, actual_distances) if abs(expected - actual) <= tolerance
                    )
                    grade += correct_distances * (20 / len(expected_distances))
            else:
                print("No DataFrame found.")
        except Exception as e:
            print(f"Distance Validation Error: {e}")

    return round(grade)
