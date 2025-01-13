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
        exec(code, globals(), local_context)
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
            # Extract all float values from the code execution context
            import re
            
            # First look for printed output containing the distances
            printed_values = []
            def mock_print(*args, **kwargs):
                printed_values.extend(str(arg) for arg in args)
            
            # Re-execute code with mocked print to capture output
            mock_globals = {'print': mock_print, **globals()}
            exec(code, mock_globals, local_context)
            
            # Look for float values in printed output
            all_numbers = []
            for output in printed_values:
                numbers = re.findall(r'\d+\.\d+', output)
                all_numbers.extend([float(num) for num in numbers])
            
            # Also look for DataFrame values
            for var in local_context.values():
                if isinstance(var, pd.DataFrame):
                    for col in var.columns:
                        if var[col].dtype in ['float64', 'float32', 'int64', 'int32']:
                            all_numbers.extend(var[col].tolist())
            
            # Round all numbers to 2 decimal places
            all_numbers = [round(num, 2) for num in all_numbers]
            
            # Expected distances
            expected_distances = [59.57, 73.14, 37.98]
            
            # Check if all expected distances are present
            matched_distances = 0
            for expected in expected_distances:
                if any(abs(actual - expected) <= 0.5 for actual in all_numbers):
                    matched_distances += 1
            
            # Award points based on matched distances
            if matched_distances == 3:
                distance_score += 20
                print("All distances correctly calculated (20/20)")
            else:
                partial_score = (matched_distances * 20) // 3
                distance_score += partial_score
                print(f"Partially correct distances ({partial_score}/20)")
                
        except Exception as e:
            print(f"Distance Validation Error: {e}")
    else:
        print("Geodesic Function: Not Detected (0/10)")

    grade += distance_score
    print(f"Distance Calculations: {distance_score}/30")

    print(f"\n=== Final Grade: {round(grade)}/100 ===\n")
    return round(grade)
