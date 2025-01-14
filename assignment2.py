# assignment2.py
import streamlit as st
import folium
import pandas as pd
import requests
from io import StringIO
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from utils.style2 import set_page_style
from Record.google_sheet import validate_student_id, update_google_sheet

def show():
    # Apply the custom page style
    set_page_style()

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "chart_object" not in st.session_state:
        st.session_state["chart_object"] = None
    if "captured_output" not in st.session_state:
        st.session_state["captured_output"] = ""

    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Student ID Validation
    st.header("Step 1: Validate Your Student ID")
    student_id = st.text_input("Enter Your Student ID", key="student_id")
    validate_button = st.button("Validate ID", key="validate_id_button")

    if validate_button:
        if validate_student_id(student_id):
            st.success("Student ID validated successfully!")
            st.session_state["validated"] = True
        else:
            st.error("Invalid Student ID. Please check your ID or contact support.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        In this assignment, you will fetch real-time earthquake data from the USGS Earthquake API, filter earthquakes with a magnitude greater than 4.0, and visualize the data on a map and bar chart.

        ### Task Requirements:
        1. **Fetch Earthquake Data:**
           - Use the USGS Earthquake API to retrieve data for the date range January 2nd, 2025, to January 9th, 2025.
           - Filter earthquakes with a magnitude greater than 4.0.
        2. **Visualize Data:**
           - Plot earthquake locations on an interactive map using `folium`.
           - Use different marker colors based on magnitude ranges:
             - Green: 4.0-5.0
             - Yellow: 5.0-5.5
             - Red: 5.5+
           - Add popups to display earthquake details (magnitude, location, time).
        3. **Generate a Bar Chart:**
           - Create a bar chart showing earthquake frequency by magnitude ranges:
             - 4.0-4.5
             - 4.5-5.0
             - 5.0+
        4. **Text Summary:**
           - Provide a CSV-formatted summary including:
             - Total number of earthquakes with magnitude > 4.0.
             - Average, maximum, and minimum magnitudes.
             - Number of earthquakes in each magnitude range.
        """)

    with tab2:
        st.markdown("""
        ### Grading Breakdown:
        - **API Data Fetching (20 points):**
          - Correctly fetch data from the USGS API.
        - **Data Filtering (10 points):**
          - Filter earthquakes with magnitude > 4.0.
        - **Map Visualization (30 points):**
          - Plot earthquake locations on a map.
          - Use appropriate marker colors and popups.
        - **Bar Chart (20 points):**
          - Generate a bar chart for earthquake frequency by magnitude ranges.
        - **Text Summary (20 points):**
          - Provide a CSV-formatted summary with required details.
        """)

    # Section 3: Code Submission and Output
    if st.session_state.get("validated", False):
        st.header("Step 3: Submit and Run Your Code")
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

        # Run Code Button
        run_button = st.button("Run Code", key="run_code_button")
        if run_button and code_input:
            st.session_state["run_success"] = False
            st.session_state["captured_output"] = ""
            try:
                # Redirect stdout to capture print statements
                captured_output = StringIO()
                import sys
                sys.stdout = captured_output

                # Execute the user's code in a controlled environment
                local_context = {}
                exec(code_input, {}, local_context)

                # Restore stdout
                sys.stdout = sys.__stdout__

                # Capture printed output
                st.session_state["captured_output"] = captured_output.getvalue()

                # Look for specific outputs (folium.Map, matplotlib chart, etc.)
                map_object = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
                chart_object = next((obj for obj in local_context.values() if isinstance(obj, plt.Figure)), None)

                # Store outputs in session state
                st.session_state["map_object"] = map_object
                st.session_state["chart_object"] = chart_object

                # Mark the run as successful
                st.session_state["run_success"] = True

            except Exception as e:
                sys.stdout = sys.__stdout__
                st.error(f"An error occurred while running your code: {e}")

        # Display Outputs
        if st.session_state["run_success"]:
            st.markdown("### 📄 Captured Output")
            if st.session_state["captured_output"]:
                st.text(st.session_state["captured_output"])
            else:
                st.write("No text output captured.")

            if st.session_state["map_object"]:
                st.markdown("### 🗺️ Map Output")
                st_folium(st.session_state["map_object"], width=700, height=500)

            if st.session_state["chart_object"]:
                st.markdown("### 📊 Bar Chart Output")
                st.pyplot(st.session_state["chart_object"])

        # Submit Code Button
        submit_button = st.button("Submit Code", key="submit_code_button")
        if submit_button:
            if not st.session_state.get("run_success", False):
                st.error("Please run your code successfully before submitting.")
            else:
                from grades.grade2 import grade_assignment
                grade = grade_assignment(code_input)
                update_google_sheet(student_id, "assignment_2", grade)
                st.success(f"Submission successful! Your grade: {grade}/100")
    else:
        st.warning("Please validate your Student ID to proceed.")
