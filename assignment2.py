import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
from utils.style2 import set_page_style
from Record.google_sheet import fetch_student_record, update_google_sheet
import traceback
import sys

def show():
    # Apply custom styles
    set_page_style()

    # Page Title
    st.title("Assignment 2: Real-Time Earthquake Analysis and Visualization")

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "dataframe_object" not in st.session_state:
        st.session_state["dataframe_object"] = None
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None
    if "captured_output" not in st.session_state:
        st.session_state["captured_output"] = ""

    # Step 1: Student ID Validation
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Student ID")
        validate_button = st.form_submit_button("Validate")
        if validate_button:
            record = fetch_student_record(student_id)
            if record:
                if record.get("assignment_2_completed", False):
                    st.warning("You have already submitted Assignment 2.")
                    st.stop()
                st.success(f"Welcome back, {record['name']}! You may proceed.")
            else:
                st.error("Invalid Student ID. Please check your ID and try again.")
                st.stop()

    # Step 2: Assignment Details and Grading Criteria
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Criteria"])

    with tab1:
        st.markdown("""
        ### Task Overview
        - Fetch earthquake data from the USGS Earthquake API for January 2nd to 9th, 2025.
        - Filter earthquakes with a magnitude > 4.0.
        - Visualize the filtered data on an interactive map.
        - Create a bar chart showing earthquake frequencies by magnitude range.
        - Provide a text summary in CSV format.
        **Expected Outputs:**
        - A map displaying earthquake locations with markers and popups.
        - A bar chart of earthquake frequencies by magnitude range.
        - A CSV summary of earthquake statistics.
        """)

    with tab2:
        st.markdown("""
        ### Grading Breakdown
        - **API Integration (20 points):** Successfully fetch data from the USGS API.
        - **Data Filtering (20 points):** Correctly filter earthquakes with a magnitude > 4.0.
        - **Map Visualization (30 points):** Create a map with color-coded markers and popups.
        - **Bar Chart (20 points):** Generate a bar chart of earthquake frequencies.
        - **Summary Statistics (10 points):** Provide a CSV with accurate statistics.
        """)

    # Step 3: Code Submission and Output
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("Paste Your Python Code Here", height=300)
    run_button = st.button("Run Code", key="run_code_button")
    submit_button = st.button("Submit Code", key="submit_code_button")

    if run_button and code_input:
        st.session_state["run_success"] = False
        st.session_state["captured_output"] = ""
        try:
            # Redirect stdout to capture output
            captured_output = StringIO()
            sys.stdout = captured_output

            # Pre-import required libraries and inject into execution context
            exec_globals = {
                "__builtins__": __builtins__,
                "requests": __import__("requests"),
                "pd": pd,
                "folium": folium,
                "plt": plt,
                "StringIO": StringIO,
            }

            # Execute user code
            exec(code_input, exec_globals)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Process outputs
            st.session_state["captured_output"] = captured_output.getvalue()
            st.session_state["map_object"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, folium.Map)), None)
            st.session_state["dataframe_object"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, pd.DataFrame)), None)
            st.session_state["bar_chart"] = plt.gcf() if plt.get_fignums() else None
            st.session_state["run_success"] = True

        except Exception as e:
            sys.stdout = sys.__stdout__
            st.error(f"An error occurred while running your code: {e}")
            st.error(traceback.format_exc())

    # Display Outputs
    if st.session_state["run_success"]:
        if st.session_state["captured_output"]:
            st.markdown("### Captured Output")
            st.text(st.session_state["captured_output"])

        if st.session_state["map_object"]:
            st.markdown("### Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["bar_chart"]:
            st.markdown("### Bar Chart Output")
            st.pyplot(st.session_state["bar_chart"])

        if st.session_state["dataframe_object"] is not None:
            st.markdown("### Data Summary")
            st.dataframe(st.session_state["dataframe_object"])

    # Submit Button
    if submit_button:
        if not code_input:
            st.error("Please paste and run your code before submitting.")
        elif st.session_state.get("run_success", False):
            from grades.grade2 import grade_assignment
            # Grade the assignment
            grade = grade_assignment(code_input)
            update_google_sheet(record["name"], record["email"], student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please run your code successfully before submitting.")

if __name__ == "__main__":
    show()
