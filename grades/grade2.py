def grade_assignment2(code):
    import re
    import pandas as pd
    import matplotlib.pyplot as plt

    grade = 0

    # 1. Library Imports (10 Points)
    required_libraries = ["folium", "matplotlib", "requests", "pandas"]
    imported_libraries = sum(1 for lib in required_libraries if lib in code)
    grade += min(10, imported_libraries * 2)

    unused_libraries = re.findall(r"import\s+(\w+)", code)
    for lib in unused_libraries:
        if lib not in required_libraries:
            grade -= 1

    # 2. Code Quality (20 Points)
    descriptive_variables = sum(1 for var in ["earthquake_map", "magnitude_counts"] if var in code)
    grade += min(5, descriptive_variables * 1.25)

    if "=" in code and not re.search(r"\s=\s", code):
        grade -= 5

    comments = len(re.findall(r"#", code))
    grade += min(5, comments * 1)

    blank_lines = len(re.findall(r"\n\n", code))
    grade += min(5, blank_lines * 1)

    # 3. Fetching Data from the API (10 Points)
    if "earthquake.usgs.gov" in code:
        grade += 3
    if "requests.get" in code or "urllib" in code:
        grade += 3
    if "response.status_code" in code:
        grade += 4

    # 4. Filtering Earthquakes (10 Points)
    if "> 4.0" in code:
        grade += 5
    if all(x in code for x in ["latitude", "longitude", "magnitude", "time"]):
        grade += 5

    # 5. Map Visualization (20 Points)
    if "folium.Map" in code:
        grade += 5
    if "folium.Marker" in code:
        if "color='green'" in code and "color='yellow'" in code and "color='red'" in code:
            grade += 9
    if "popup" in code:
        grade += 6

    # 6. Bar Chart (15 Points)
    if "plt.bar" in code:
        grade += 5
    if "4.0-4.5" in code and "4.5-5.0" in code and ">5.0" in code:
        grade += 9
    if all(label in code for label in ["plt.xlabel", "plt.ylabel", "plt.title"]):
        grade += 1

    # 7. Text Summary (15 Points)
    if "total earthquakes" in code.lower():
        grade += 3
    if all(metric in code.lower() for metric in ["average", "maximum", "minimum"]):
        grade += 9
    if "4.0-4.5" in code.lower() and "4.5-5.0" in code.lower() and "5.0+" in code.lower():
        grade += 3

    # 8. Overall Execution (10 Points)
    try:
        local_context = {}
        exec(code, {}, local_context)

        if "folium.Map" in code and "plt.bar" in code:
            grade += 5

        # Check outputs
        if any(isinstance(obj, pd.DataFrame) for obj in local_context.values()):
            grade += 5
    except Exception as e:
        grade -= 5

    return max(0, round(grade))
