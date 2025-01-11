import streamlit as st
from utils.style1 import set_page_style
from grades.grade1 import grade_assignment
from Record.google_sheet import update_google_sheet
import uuid

# Set the page style
set_page_style()

# Generate a unique Student ID
def generate_student_id(name, email):
    unique_id = str(uuid.uuid4().int)[:4] + email[0].upper()
    return unique_id

# Streamlit UI
st.title("Assignment 1: Mapping Coordinates and Calculating Distances")

# Student Information Form
with st.form("student_form", clear_on_submit=False):
    # Fields for student information
    full_name = st.text_input("Full Name", key="full_name")
    email = st.text_input("Email", key="email")
    student_id = generate_student_id(full_name, email) if full_name and email else "N/A"
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
        exec(code_input)
        st.success("Code executed successfully. Check the map and output summary.")
    except Exception as e:
        st.error(f"Error executing code: {e}")

# Submit and grade
if submit_button and code_input:
    grade = grade_assignment(code_input)
    update_google_sheet(full_name, email, student_id, grade, "assignment_1")
    st.success(f"Submission successful! Your grade: {grade}/100")
