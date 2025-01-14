import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys
from utils.style2 import set_page_style
from Record.google_sheet import fetch_student_record, update_google_sheet
from grades.grade2 import grade_assignment

def execute_user_code(code_input):
    """
    Executes the user-provided code and captures outputs.
    Returns a dictionary containing captured outputs, map object, dataframe object, and bar chart.
    """
    captured_output = StringIO()
    local_context = {
        "pd": pd,
        "folium": folium,
        "plt": plt,
        "StringIO": StringIO,
    }
    sys.stdout = captured_output  # Redirect stdout to capture print statements

    try:
        exec(code_input, {}, local_context)  # Execute user code in an isolated context
        sys.stdout = sys.__stdout__  # Restore stdout

        # Extract outputs from the local context
        map_object = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
        dataframe_object = next((obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None)
        bar_chart = plt.gcf() if plt.get_fignums() else None

        return {
            "captured_output": captured_output.getvalue(),
            "map_object": map_object,
            "dataframe_object": dataframe_object,
            "bar_chart": bar_chart,
            "success": True,
        }
    except Exception as e:
        sys.stdout = sys.__stdout__  # Restore stdout
        return {
            "captured_output": traceback.format_exc(),  # Capture traceback for debugging
            "map_object": None,
            "dataframe_object": None,
            "bar_chart": None,
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
    if "dataframe_object" not in st.session_state:
        st.session_state["dataframe_object"] = None
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None

    # Page Title
    st.title("Assignment 2: Real-Time Earthquake Analysis and Visualization")

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

    # Run Code Button
    run_button = st.button("Run Code", key="run_code_button")
    if run_button and code_input:
        st.session_state["run_success"] = False
        st.session_state["captured_output"] = ""
        st.session_state["map_object"] = None
        st.session_state["dataframe_object"] = None
        st.session_state["bar_chart"] = None

        # Execute user code
        result = execute_user_code(code_input)

        # Update session state with results
        st.session_state["captured_output"] = result["captured_output"]
        st.session_state["map_object"] = result["map_object"]
        st.session_state["dataframe_object"] = result["dataframe_object"]
        st.session_state["bar_chart"] = result["bar_chart"]
        st.session_state["run_success"] = result["success"]

        if result["success"]:
            st.success("Code executed successfully!")
        else:
            st.error("An error occurred while executing the code.")

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
    submit_button = st.button("Submit Assignment", key="submit_assignment")
    if submit_button:
        if not code_input:
            st.error("Please paste and run your code before submitting.")
        elif st.session_state.get("run_success", False):
            try:
                grade = grade_assignment(code_input)
                update_google_sheet(record["name"], record["email"], student_id, grade, "assignment_2")
                st.success(f"Submission successful! Your grade: {grade}/100")
            except Exception as e:
                st.error(f"An error occurred while updating the Google Sheet: {e}")
        else:
            st.error("Please run your code successfully before submitting.")

if __name__ == "__main__":
    show()
