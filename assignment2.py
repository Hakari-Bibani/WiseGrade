import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys
from Record.google_sheet import get_student_ids, update_google_sheet
from grades.grade2 import grade_assignment2
from utils.style2 import set_page_style  # Import the style function

def show():
    # Apply the custom page style
    set_page_style()  # Apply the styles from style2.py

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

    st.title("Assignment 2: Earthquake Data Analysis")

    # Fetch valid student IDs from Google Sheet
    valid_student_ids = get_student_ids()  # Ensure this returns a list of valid IDs

    # Section 1: Student ID Form
    st.header("Step 1: Enter Your Student ID")
    valid_student_id = False
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id in valid_student_ids:
                st.success(f"Student ID {student_id} verified. You may proceed.")
                valid_student_id = True
            else:
                st.error("Invalid Student ID. Please ensure you are using the ID saved in Assignment 1.")
                return

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        Write a Python script that fetches real-time earthquake data from the USGS Earthquake API, filters earthquakes with a magnitude greater than 4.0, and visualizes the data on a map and as a bar chart.
        
        **Key Tasks:**
        1. Fetch earthquake data from the USGS API for the date range January 2nd, 2025, to January 9th, 2025.
        2. Filter earthquakes with a magnitude greater than 4.0.
        3. Visualize locations on a map with markers color-coded by magnitude range.
        4. Create a bar chart showing earthquake counts by magnitude ranges.
        5. Provide a text summary of the results.
        """)

    with tab2:
        st.markdown("""
        ### Grading Criteria
        - **Code Correctness (50%)**: The code should run without errors and produce the correct outputs.
        - **Visualization Quality (30%)**: The map and bar chart should be clear and informative.
        - **Code Quality (20%)**: The code should be well-structured, readable, and commented.
        """)

    # Section 3: Code Editor
    st.header("Step 3: Write and Run Your Code")
    code = st.text_area("Write your Python code here", height=300)

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["dataframe_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["captured_output"] = ""

        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            exec(code)
            st.session_state["run_success"] = True
            st.session_state["captured_output"] = new_stdout.getvalue()
            st.success("Code executed successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state["captured_output"] = traceback.format_exc()
        finally:
            sys.stdout = old_stdout

        # Display captured output
        st.text_area("Code Output", st.session_state["captured_output"], height=200)

    # Section 4: Visualize Outputs
    st.header("Step 4: Visualize Your Outputs")
    if st.session_state.get("map_object"):
        st_folium(st.session_state["map_object"], width=700, height=500)
    if st.session_state.get("dataframe_object") is not None:
        st.dataframe(st.session_state["dataframe_object"])
    if st.session_state.get("bar_chart"):
        st.pyplot(st.session_state["bar_chart"])

    # Section 5: Submit Assignment
    st.header("Step 5: Submit Your Assignment")
    submit_button = st.button("Submit Assignment")

    if submit_button:
        if st.session_state.get("run_success", False) and valid_student_id:
            try:
                # Grade the assignment
                grade = grade_assignment2(code)  # Use the user's code input
                st.success(f"Submission successful! Your grade: {grade}/100")

                # Update Google Sheet
                update_google_sheet(
                    student_id=student_id,
                    assignment_name="assignment_2",
                    grade=grade
                )
            except Exception as e:
                st.error(f"Failed to update Google Sheets: {e}")
        else:
            st.error("Please ensure your Student ID is verified and the code runs successfully before submitting.")

if __name__ == "__main__":
    show()
