import streamlit as st

# Function to grade the assignment
def grade_assignment(code):
    grade = 0

    # a. Library Imports (5 points: 1.25 points per library)
    required_imports = ["folium", "geopy", "geodesic", "pandas"]
    imported_libraries = sum(1 for lib in required_imports if lib in code)
    grade += min(5, imported_libraries * 1.25)  # Maximum 5 points

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

# Streamlit App Layout
st.title("Assignment Grading System")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Assignment Description", "Grading Breakdown", "Submit Assignment"])

# Tab 1: Assignment Description
with tab1:
    st.markdown("""
    ### Objective
    In this assignment, you will write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers. This will help you practice working with geospatial data and Python libraries for mapping and calculations.

    ### Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python
    **Objective:**
    In this assignment, you will write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers. This will help you practice working with geospatial data and Python libraries for mapping and calculations.
    """)
    # Add "See More" expandable section
    with st.expander("See More"):
        st.markdown("""
    **Task Requirements:**
    1. **Plot the Three Coordinates on a Map:**
       - The coordinates represent three locations in the Kurdistan Region.
       - You will use Python libraries to plot these points on a map.
       - The map should visually display the exact locations of the coordinates.

    2. **Calculate the Distance Between Each Pair of Points:**
       - You will calculate the distances between the three points in kilometers.
       - Specifically, calculate:
         - The distance between Point 1 and Point 2.
         - The distance between Point 2 and Point 3.
         - The distance between Point 1 and Point 3.
       - Add Markers to the map for each coordinate.
       - Add polylines to connect the points.
       - Add popups to display information about the distance.

    **Coordinates:**
    - Point 1: Latitude: 36.325735, Longitude: 43.928414
    - Point 2: Latitude: 36.393432, Longitude: 44.586781
    - Point 3: Latitude: 36.660477, Longitude: 43.840174

    **Python Libraries You Will Use:**
    - `geopy` for calculating the distance between two coordinates.
    - `folium` for plotting the points on an interactive map.
    - `pandas` to create a DataFrame that displays the distances between the points.

    **Expected Output:**
    1. A map showing the three coordinates.
    2. A text summary (Express values to two decimal places.): showing the calculated distances (in kilometers) between:
       - Point 1 and Point 2.
       - Point 2 and Point 3.
       - Point 1 and Point 3.
    """)

# Tab 2: Grading Breakdown
with tab2:
    st.markdown("""
    ### Detailed Grading Breakdown

    #### 1. Code Structure and Implementation (30 points)
    - **Library Imports (5 points):**
        - Checks if the required libraries (`folium`, `geopy`, `geodesic`) are imported.
    - **Coordinate Handling (5 points):**
        - Checks if the correct coordinates are defined in the code.
    - **Code Execution (10 points):**
        - Checks if the code runs without errors.
    - **Code Quality (10 points):**
        - **Variable Naming:** 2 points (deducted if single-letter variables are used).
        - **Spacing:** 2 points (deducted if improper spacing is found, e.g., no space after `=`).
        - **Comments:** 2 points (deducted if no comments are present).
        - **Code Organization:** 2 points (deducted if no blank lines are used for separation).
    """)
    # Add "See More" expandable section
    with st.expander("See More"):
        st.markdown("""
    #### 2. Map Visualization (40 points)
    - **Map Generation (15 points):**
        - Checks if the `folium.Map` is correctly initialized.
    - **Markers (15 points):**
        - Checks if markers are added to the map for each coordinate.
    - **Polylines (5 points):**
        - Checks if polylines are used to connect the points.
    - **Popups (5 points):**
        - Checks if popups are added to the markers.

    #### 3. Distance Calculations (30 points)
    - **Geodesic Implementation (10 points):**
        - Checks if the `geodesic` function is used correctly to calculate distances.
    - **Distance Accuracy (20 points):**
        - Checks if the calculated distances are accurate within a 100-meter tolerance.
    """)

# Tab 3: Submit Assignment
with tab3:
    st.header("Submit Your Assignment")
    user_code = st.text_area("Paste your Python code here:", height=300)
    if st.button("Submit"):
        if user_code.strip():
            grade = grade_assignment(user_code)
            st.success(f"Your grade is: {grade}/100")
        else:
            st.error("Please paste your code before submitting.")
