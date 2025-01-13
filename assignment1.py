# assignment1.py
import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import set_page_style

def generate_student_id(name, email):
    """Generate a unique student ID based on name and email."""
    import random
    import string
    if name and email:
        random_numbers = ''.join(random.choices(string.digits, k=4))
        random_letter = random.choice(string.ascii_uppercase)
        return random_numbers + random_letter
    return "N/A"

def show():
    # Apply the custom page style
    set_page_style()

    st.title("Assignment 1: Mapping Coordinates and Calculating Distances")

    # Split UI into three sections
    col1, col2 = st.columns([1, 2])

    # Section 1: Student Information
    with col1:
        st.header("Student Information")
        with st.form("student_form", clear_on_submit=False):
            # Fields for student information
            full_name = st.text_input("Full Name", key="full_name")
            email = st.text_input("Email", key="email")

            # Generate Student ID dynamically
            student_id = generate_student_id(full_name, email)
            st.write(f"Student ID: {student_id}")

            # Submit button for the form
            submit_info_button = st.form_submit_button("Save Information")

    # Section 2: Tabs for Assignment and Grading Details
    with col2:
        st.header("Assignment Details and Grading")
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("""
            ### Objective
            In this assignment, you will write a Python script to:
            1. Plot three geographical coordinates on a map.
            2. Calculate the distances between each pair of points in kilometers.

            ### Task Requirements
            - Add markers for each coordinate.
            - Draw polylines connecting the points.
            - Use popups to display the distances between points.

            ### Coordinates
            - Point 1: Latitude: 36.325735, Longitude: 43.928414
            - Point 2: Latitude: 36.393432, Longitude: 44.586781
            - Point 3: Latitude: 36.660477, Longitude: 43.840174

            Use Python libraries like `folium`, `geopy`, and `pandas` for the task.
            """)

        with tab2:
            st.markdown("""
            ### Detailed Grading Breakdown

            #### 1. Code Structure and Implementation (30 points)
            - **Library Imports (5 points)**
            - **Coordinate Handling (5 points)**
            - **Code Execution (10 points)**
            - **Code Quality (10 points)**

            #### 2. Map Visualization (40 points)
            - **Map Generation (15 points)**
            - **Markers (15 points)**
            - **Polylines (5 points)**
            - **Popups (5 points)**

            #### 3. Distance Calculations (30 points)
            - **Geodesic Implementation (10 points)**
            - **Distance Accuracy (20 points)**
            """)

    # Section 3: Code Submission and Execution
    st.header("Code Submission")
    code_input = st.text_area("**📝 Paste Your Code Here**")

    # Run and Submit Buttons
    run_button = st.button("Run Code")
    submit_button = st.button("Submit Code", disabled=True)

    # Execute the code
    if run_button:
        if not code_input.strip():
            st.warning("Please paste your Python script to run.")
        else:
            try:
                # Create a local dictionary to capture code execution results
                local_context = {}
                exec(code_input, {}, local_context)

                # Search for outputs
                map_object = next((var for var in local_context.values() if isinstance(var, folium.Map)), None)
                dataframe_object = next((var for var in local_context.values() if isinstance(var, pd.DataFrame)), None)

                # Display outputs
                if map_object:
                    st.success("Map generated successfully!")
                    st_folium(map_object, width=700, height=500)
                else:
                    st.warning("No Folium map found in the code output.")

                if dataframe_object is not None:
                    st.markdown("### 📏Distance Summary")
                    st.dataframe(dataframe_object)

                # Enable submission after successful run
                submit_button = st.button("Submit Code", disabled=False)

            except Exception as e:
                st.error("An error occurred while executing your code:")
                st.error(str(e))

    # Submit and grade
    if submit_button:
        if full_name and email:
            from grades.grade1 import grade_assignment
            from Record.google_sheet import update_google_sheet

            grade = grade_assignment(code_input)
            update_google_sheet(full_name, email, student_id, grade, "assignment_1")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please fill out both 'Full Name' and 'Email' to generate your Student ID.")
