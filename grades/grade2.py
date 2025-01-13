import re
import pandas as pd

def grade_assignment_2(code):
    """Grade Assignment 2 based on the specified rubric."""
    grade = 0

    # 1. Library Imports (10 Points)
    required_imports = ["folium", "matplotlib", "seaborn", "requests", "pandas"]
    for lib in required_imports:
        if lib in code:
            grade += 2
        else:
            grade -= 2

    unused_libraries = [lib for lib in re.findall(r"import (\w+)", code) if lib not in required_imports]
    grade -= len(unused_libraries)

    # 2. Code Quality (20 Points)
    # Variable Naming
    descriptive_variables = ["earthquake_map", "magnitude_counts"]
    grade += 5 if all(var in code for var in descriptive_variables) else -5

    # Spacing
    if "=" in code.replace(" = ", "") or any(op in code.replace(f" {op} ", "") for op in [">", "<"]):
        grade -= 5

    # Comments
    if code.count("#") >= 5:
        grade += 5
    else:
        grade -= 5

    # Code Organization
    grade += 5 if "\n\n" in code else -3

    # 3. Fetching Data from the API (10 Points)
    if "https://earthquake.usgs.gov/fdsnws/event/1/query" in code:
        grade += 3
    else:
        grade -= 3

    if "requests.get" in code or "urllib" in code:
        grade += 3
    else:
        grade -= 3

    if "response.status_code" in code:
        grade += 4
    else:
        grade -= 4

    # 4. Filtering Earthquakes (10 Points)
    if "magnitude > 4.0" in code:
        grade += 5
    else:
        grade -= 5

    if all(field in code for field in ["latitude", "longitude", "magnitude", "time"]):
        grade += 5
    else:
        grade -= 5

    # 5. Map Visualization (20 Points)
    if "folium.Map" in code:
        grade += 5

    color_coding = {
        "green": "4.0 <= mag < 5.0",
        "yellow": "5.0 <= mag <= 5.5",
        "red": "mag > 5.5"
    }
    for color, logic in color_coding.items():
        if color in code and logic in code:
            grade += 3

    if all(info in code for info in ["popup=", "latitude", "longitude", "time"]):
        grade += 6

    # 6. Bar Chart (15 Points)
    if "plt.bar" in code or "sns.barplot" in code:
        grade += 5

    ranges = ["4.0-4.5", "4.5-5.0", ">5.0"]
    if all(range in code for range in ranges):
        grade += 9
    else:
        grade -= 3

    if all(label in code for label in ["xlabel", "ylabel", "title"]):
        grade += 1

    # 7. Text Summary (15 Points)
    summary_metrics = ["total_earthquakes", "avg_magnitude", "max_magnitude", "min_magnitude"]
    if all(metric in code for metric in summary_metrics):
        grade += 12
    else:
        grade -= 3

    if ".to_csv" in code:
        grade += 5
    else:
        grade -= 5

    # 8. Overall Execution (10 Points)
    try:
        local_context = {}
        exec(code, {}, local_context)
        grade += 5  # Script runs without errors

        outputs = [
            "folium.Map",  # Map
            "plt.bar",  # Bar chart
            "pandas.DataFrame.to_csv"  # Summary saved as CSV
        ]
        if all(output in code for output in outputs):
            grade += 5
        else:
            grade -= 3

    except Exception as e:
        print(f"Execution Error: {e}")
        grade -= 5

    return max(0, round(grade))
