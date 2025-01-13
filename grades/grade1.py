def grade_assignment(code):
    # Previous grading code remains the same...

    # Modified Distance Calculations section
    distance_score = 0
    if "geodesic" in code:
        distance_score += 10
        print("Geodesic Function: Detected (10/10)")
        try:
            dataframe_object = next((obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None)
            if dataframe_object is not None:
                print("DataFrame Detected")
                
                # Get all numeric columns
                numeric_cols = dataframe_object.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns
                
                expected_distances = [59.57, 73.14, 37.98]
                found_distances = False
                
                # Check each numeric column for the expected distances
                for col in numeric_cols:
                    values = dataframe_object[col].round(2).tolist()
                    # Sort both lists to compare values regardless of order
                    values.sort()
                    expected_distances_sorted = sorted(expected_distances)
                    
                    # Check if values match expected distances
                    if all(abs(a - b) <= 0.5 for a, b in zip(values, expected_distances_sorted)):
                        print(f"Correct distances found in column: {col}")
                        distance_score += 20  # Full points for correct distances
                        found_distances = True
                        break
                
                if not found_distances:
                    print("Expected distances not found in any column")
                    print(f"Expected distances: {expected_distances}")
                    print(f"Found values: {[dataframe_object[col].tolist() for col in numeric_cols]}")
            else:
                print("No DataFrame Detected")
        except Exception as e:
            print(f"Distance Validation Error: {e}")
    else:
        print("Geodesic Function: Not Detected (0/10)")

    grade += distance_score
    print(f"Distance Calculations: {distance_score}/30")

    # Rest of the grading code remains the same...

    print(f"\n=== Final Grade: {round(grade)}/100 ===\n")
    return round(grade)
