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

    # Student Information Form (split from the rest of the content)
    with st.container():
        st.markdown("### Student Information")
        with st.form("student_info_form", clear_on_submit=False):
            full_name = st.text_input("Full Name", key="full_name")
            email = st.text_input("Email", key="email")
            student_id = generate_student_id(full_name, email)
            st.write(f"Student ID: {student_id}")
            st.form_submit_button("Save Student Info")

    # Tabs for assignment and grading details (split from student info)
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        Plot three geographical coordinates on a map and calculate the distances between them in kilometers.
        #### Coordinates:
        - Point 1: Latitude: 36.325735, Longitude: 43.928414
        - Point 2: Latitude: 36.393432, Longitude: 44.586781
        - Point 3: Latitude: 36.660477, Longitude: 43.840174
        """)
        st.markdown("Expand for detailed instructions...")

    with tab2:
        st.markdown("""
        #### Grading Breakdown
        - Library Imports: 5 points
        - Coordinate Handling: 5 points
        - Code Execution: 10 points
        - Map Visualization: 40 points
        - Distance Calculations: 30 points
        """)

    # Code Submission Area (split from student info)
    st.markdown("### Code Submission")
    code_input = st.text_area("Paste Your Code Here", height=200)

    # Buttons for Run and Submit
    run_button = st.button("Run")
    submit_button = st.button("Submit")

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
                st.markdown("### Generated Map")
                st.components.v1.html(map_object._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the code output.")

            if dataframe_object is not None:
                st.markdown("### Distance Summary")
                st.write(dataframe_object)
            else:
                st.warning("No DataFrame with distances found in the code output.")

        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())

    # Submit and grade (only allowed after running)
    if submit_button and code_input:
        if not run_button:
            st.error("Please run your code before submitting.")
        elif full_name and email:
            grade = grade_assignment(code_input)
            update_google_sheet(full_name, email, student_id, grade, "assignment_1")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please fill out both 'Full Name' and 'Email' to generate your Student ID.")
