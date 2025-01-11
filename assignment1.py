import streamlit as st
from utils.style1 import set_page_style
from grades.grade1 import grade_assignment
from Record.google_sheet import update_google_sheet
import random
import string
import traceback

# Set the page style
set_page_style()

# Generate a unique Student ID
def generate_student_id(name, email):
    if name and email:
        random_numbers = ''.join(random.choices(string.digits, k=4))
        random_letter = random.choice(string.ascii_uppercase)
        return random_numbers + random_letter
    return "N/A"

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

        # Code Submission Area
        code_input = st.text_area("Paste Your Code Here")

        # Form Submit Buttons
        run_button = st.form_submit_button("Run")
        submit_button = st.form_submit_button("Submit")

    # Execute the code
    if run_button and code_input:
        try:
            # Create a local dictionary to capture code execution results
            local_context = {}
            exec(code_input, {}, local_context)

            # Check for expected outputs (map and summary text)
            if "map_kurdistan" in local_context and "df_distances" in local_context:
                st.success("Code executed successfully!")
                
                # Display the map
                map_object = local_context["map_kurdistan"]
                map_object.save("map_kurdistan.html")
                st.markdown("### Generated Map")
                st.components.v1.html(map_object._repr_html_(), height=500)

                # Display the distance summary
                st.markdown("### Distance Summary")
                df_distances = local_context["df_distances"]
                st.write(df_distances)
            else:
                st.warning("Your code executed without errors, but the expected outputs (map and distances) were not found.")
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
