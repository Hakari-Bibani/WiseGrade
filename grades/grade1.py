import streamlit as st

def calculate_grade(code):
    # Placeholder grading logic (replace with actual grading criteria)
    grade = 0

    # Check if required libraries are imported
    if "import folium" in code and "from geopy.distance import geodesic" in code:
        grade += 5  # Library Imports

    # Check if coordinates are defined
    if "point1" in code and "point2" in code and "point3" in code:
        grade += 5  # Coordinate Handling

    # Check if code runs without errors
    try:
        exec(code)
        grade += 10  # Code Execution
    except:
        pass

    # Check code quality (basic checks)
    if "=" in code and "#" in code and "\n\n" in code:
        grade += 10  # Code Quality

    # Check map visualization components
    if "folium.Map" in code and "folium.Marker" in code and "folium.PolyLine" in code:
        grade += 40  # Map Visualization

    # Check distance calculations
    if "geodesic(point1, point2)" in code:
        grade += 30  # Distance Calculations

    return grade

# Streamlit UI for grading
st.title("Assignment 1 Grading")

# Input field for code
code = st.text_area("Paste your Python code here:", height=300)

if st.button("Calculate Grade"):
    if code:
        grade = calculate_grade(code)
        st.success(f"Your grade for Assignment 1 is: {grade}/100")
    else:
        st.warning("Please paste your code before calculating the grade.")
