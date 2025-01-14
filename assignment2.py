import streamlit as st
import folium
import pandas as pd
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import validate_student_id, update_google_sheet

def execute_user_code(code_input):
    """
    Executes the user-provided code and captures outputs.
    Returns a dictionary containing captured outputs, map object, and image object.
    """
    captured_output = StringIO()
    local_context = {}
    sys.stdout = captured_output  # Redirect stdout to capture print statements

    try:
        exec(code_input, {}, local_context)  # Execute user code in an isolated context
        sys.stdout = sys.__stdout__  # Restore stdout

        # Extract outputs from the local context
        map_object = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
        image_object = local_context.get("image_object", None)

        return {
            "captured_output": captured_output.getvalue(),
            "map_object": map_object,
            "image_object": image_object,
            "success": True,
        }
    except Exception as e:
        sys.stdout = sys.__stdout__  # Restore stdout
        return {
            "captured_output": traceback.format_exc(),  # Capture traceback for debugging
            "map_object": None,
            "image_object": None,
            "success": False,
        }

def show():
    # Apply custom styles
    set_page_style()

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "captured_output" not in st.session_state:
        st.session_state["captured_output"] = ""
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "image_object" not in st.session_state:
        st.session_state["image_object"] = None

    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Student ID Form
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id and validate_student_id(student_id):  # Validate student ID
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        Fetch real-time earthquake data, process it, and visualize it through maps and charts.
        **Requirements:**
        - Use the USGS Earthquake API to fetch data.
        - Filter earthquakes with magnitude > 4.0.
        - Create an interactive map with earthquake locations and popups.
        - Visualize earthquake frequency as a bar chart.
        - Provide a text summary (e.g., number of earthquakes, average magnitude, etc.).
        """)

    with tab2:
        st.markdown("""
        ### Grading Breakdown
        1. **Code Implementation (30 points)**:
           - Imports, API integration, and data filtering.
        2. **Visualization (40 points)**:
           - Map, markers, popups, and bar chart.
        3. **Summary (30 points)**:
           - Accurate text-based statistics.
        """)

    # Section 3: Code Submission and Output
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

    # Run Code Button
    run_button = st.button("Run Code", key="run_code_button")
    if run_button and code_input:
        st.session_state["run_success"] = False
        st.session_state["captured_output"] = ""
        st.session_state["map_object"] = None
        st.session_state["image_object"] = None

        # Execute user code
        result = execute_user_code(code_input)

        # Update session state with results
        st.session_state["captured_output"] = result["captured_output"]
        st.session_state["map_object"] = result["map_object"]
        st.session_state["image_object"] = result["image_object"]
        st.session_state["run_success"] = result["success"]

        if result["success"]:
            st.success("Code executed successfully!")
        else:
            st.error("An error occurred while executing the code.")

    # Display Outputs
    if st.session_state["run_success"]:
        st.markdown("### 📄 Captured Output")
        st.text(st.session_state["captured_output"])

        if st.session_state["map_object"]:
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["image_object"]:
            st.markdown("### 📊 Bar Chart Output")
            st.image(st.session_state["image_object"])

    # Submit Code Button
    submit_button = st.button("Submit Code", key="submit_code_button")
    if submit_button:
        if st.session_state["run_success"]:
            try:
                grade = grade_assignment(code_input)
                update_google_sheet(student_id, grade, "assignment_2")
                st.success(f"Submission successful! Your grade: {grade}/100")
            except Exception as e:
                st.error(f"An error occurred while updating the Google Sheet: {e}")
        else:
            st.error("Please run your code successfully before submitting.")

if __name__ == "__main__":
    show()
