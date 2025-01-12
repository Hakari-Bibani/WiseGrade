import streamlit as st
from utils.style1 import set_page_style
from grades.grade1 import grade_assignment
from Record.google_sheet import update_google_sheet
import random
import string
import traceback
import folium
import pandas as pd

# Set the page style
set_page_style()

# Generate a unique Student ID
def generate_student_id(name, email):
    if name and email:
        random_numbers = ''.join(random.choices(string.digits, k=4))
        random_letter = random.choice(string.ascii_uppercase)
        return random_numbers + random_letter
    return "N/A"

def find_folium_map(local_context):
    """Search for a Folium map object in the local context."""
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            return var_value
    return None

def find_dataframe(local_context):
    """Search for a Pandas DataFrame or similar in the local context."""
    for var_name, var_value in local_context.items():
        if isinstance(var_value, pd.DataFrame):
            return var_value
    return None

def show():
    st.title("Assignment 1: Mapping Coordinates and Calculating Distances")

    # Student Information Form
    with st.form("student_form", clear_on_submit=False):
        # Fields for student information
        full_name = st.text_input("Full Name", key="full_name")
        email = st.text_input("Email", key="email")

        # Generate Student ID dynamically
        student_id = generate_student_id(full_name, email)
        st.write(f"Student ID: {student_id}")

        # Tabs for assignment and grading details
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

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
            -  `pandas` to create a DataFrame that displays the distances between the points.

            **Expected Output:**
            1. A map showing the three coordinates.
            2. A text summary (Express values to two decimal places.): showing the calculated distances (in kilometers) between:
               - Point 1 and Point 2.
               - Point 2 and Point 3.
               - Point 1 and Point 3.
            """)


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



        # Code Submission Area
        # Bold text in st.text_area using Markdown
        code_input = st.text_area("📝 Paste Your Code Here")

        # Form Submit Buttons
        run_button = st.form_submit_button("Run")
        submit_button = st.form_submit_button("Submit")

    # Execute the code
    if run_button and code_input:
        try:
            # Create a local dictionary to capture code execution results
            local_context = {}
            exec(code_input, {}, local_context)

            # Search for outputs
            map_object = find_folium_map(local_context)
            dataframe_object = find_dataframe(local_context)

            # Display outputs
            if map_object:
                st.success("Map generated successfully!")
                map_object.save("map_kurdistan.html")
                st.markdown("### 🗺️Generated Map")
                st.components.v1.html(map_object._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the code output.")

            if dataframe_object is not None:
                st.markdown("### 📏Distance Summary")
                st.write(dataframe_object)
            else:
                st.warning("No DataFrame with distances found in the code output.")

        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())

    # Submit and grade
    if submit_button and code_input:
        if full_name and email:
            grade = grade_assignment(code_input)
            update_google_sheet(full_name, email, student_id, grade, "assignment_1")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please fill out both 'Full Name' and 'Email' to generate your Student ID.") 
