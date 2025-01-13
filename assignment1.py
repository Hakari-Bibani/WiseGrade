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

    # Split the UI into three parts: Information, Tabs, and Code Space

    # Part 1: Information Section
    with st.container():
        st.header("Student Information")
        with st.form("student_form", clear_on_submit=False):
            # Fields for student information
            full_name = st.text_input("Full Name", key="full_name")
            email = st.text_input("Email", key="email")

            # Generate Student ID dynamically
            student_id = generate_student_id(full_name, email)
            st.write(f"Student ID: {student_id}")

    # Part 2: Assignment and Grading Details (Tabs)
    with st.container():
        st.header("Assignment and Grading Details")
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

    # Part 3: Code Space
    with st.container():
        st.header("Code Submission and Output")

        # Code Submission Area
        code_input = st.text_area("**📝 Paste Your Code Here**")

        # Buttons for running and submitting code
        run_button = st.button("Run Code")
        submit_button = st.button("Submit")

        # Ensure students must run the code before submitting
        if not run_button and submit_button:
            st.error("You must run your code and verify the outputs before submitting.")

        # Execute the code
        if run_button and code_input:
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
                else:
                    st.warning("No DataFrame with distances found in the code output.")

            except Exception as e:
                st.error("An error occurred while executing your code:")
                st.error(str(e))

        # Submit and grade
        if submit_button and run_button and code_input:
            if full_name and email:
                from grades.grade1 import grade_assignment
                from Record.google_sheet import update_google_sheet

                grade = grade_assignment(code_input)
                update_google_sheet(full_name, email, student_id, grade, "assignment_1")
                st.success(f"Submission successful! Your grade: {grade}/100")
            else:
                st.error("Please fill out both 'Full Name' and 'Email' to generate your Student ID.")
