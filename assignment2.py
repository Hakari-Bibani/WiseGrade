# assignment2.py
import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
from utils.style1 import set_page_style

def show():
    # Apply the custom page style
    set_page_style()

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "bar_chart_image" not in st.session_state:
        st.session_state["bar_chart_image"] = None
    if "text_summary" not in st.session_state:
        st.session_state["text_summary"] = None

    st.title("Assignment 2: Earthquake Data Visualization")

    # Section 1: Student Information Form
    st.header("Step 1: Enter Your Details")
    with st.form("student_form", clear_on_submit=False):
        full_name = st.text_input("Full Name", key="full_name")
        email = st.text_input("Email", key="email")

        generate_id_button = st.form_submit_button("Generate Student ID")

        if generate_id_button:
            if full_name and email:
                student_id = generate_student_id(full_name, email)
                st.success(f"Student ID generated: {student_id}")
            else:
                st.error("Please provide both Full Name and Email to generate a Student ID.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        In this assignment, you will write a Python script to fetch real-time earthquake data from the USGS Earthquake API, process the data to filter earthquakes with a magnitude greater than 4.0, and plot the earthquake locations on a map. Additionally, you will calculate the number of earthquakes in different magnitude ranges and present the results visually.

        ### Task Requirements:
        - Fetch earthquake data for the date range January 2nd, 2025, to January 9th, 2025.
        - Filter the data to include only earthquakes with a magnitude greater than 4.0.
        - Create an interactive map showing the locations of the filtered earthquakes.
        - Mark earthquake locations with markers, using different colors based on their magnitude.
        - Add popups to display additional information about each earthquake (magnitude, location, and time).
        - Generate a bar chart showing earthquake frequency by magnitude ranges.
        - Provide a text summary of the earthquake data.
        """)

    with tab2:
        st.markdown("""
        ### Detailed Grading Breakdown
        - **API Data Fetching (20 points):**
            - Correctly fetch data from the USGS Earthquake API.
        - **Data Filtering (10 points):**
            - Filter earthquakes with magnitude > 4.0.
        - **Map Visualization (30 points):**
            - Create an interactive map with markers and popups.
        - **Bar Chart (20 points):**
            - Generate a bar chart showing earthquake frequency by magnitude ranges.
        - **Text Summary (20 points):**
            - Provide a text summary with total earthquakes, average/max/min magnitudes, and counts by magnitude ranges.
        """)

    # Section 3: Code Submission and Output
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

    # Run Code Button
    run_button = st.button("Run Code", key="run_code_button")
    if run_button and code_input:
        st.session_state["run_success"] = False
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

            # Look for specific outputs (map_object, bar_chart_figure, text_summary)
            map_object = local_context.get("map_object", None)
            bar_chart_figure = local_context.get("bar_chart_figure", None)
            text_summary = local_context.get("text_summary", None)

            # Store outputs in session state
            st.session_state["map_object"] = map_object
            st.session_state["bar_chart_image"] = bar_chart_figure
            st.session_state["text_summary"] = text_summary

            # Mark the run as successful
            st.session_state["run_success"] = True

        except Exception as e:
            sys.stdout = sys.__stdout__
            st.error(f"An error occurred while running your code: {e}")

    # Display Outputs
    if st.session_state["run_success"]:
        st.markdown("### 🗺️ Map Output")
        if st.session_state["map_object"]:
            st_folium(st.session_state["map_object"], width=700, height=500)
        else:
            st.warning("No map object found in the script.")

        st.markdown("### 📊 Bar Chart Output")
        if st.session_state["bar_chart_image"]:
            st.pyplot(st.session_state["bar_chart_image"])
        else:
            st.warning("No bar chart figure found in the script.")

        st.markdown("### 📄 Text Summary")
        if st.session_state["text_summary"]:
            st.text(st.session_state["text_summary"])
        else:
            st.warning("No text summary found in the script.")

    # Submit Code Button
    submit_button = st.button("Submit Code", key="submit_code_button")
    if submit_button:
        if not st.session_state.get("run_success", False):
            st.error("Please run your code successfully before submitting.")
        elif full_name and email:
            from grades.grade2 import grade_assignment
            from Record.google_sheet import update_google_sheet

            grade = grade_assignment(code_input)
            student_id = generate_student_id(full_name, email)
            update_google_sheet(full_name, email, student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please ensure Full Name and Email are entered to submit.")


def generate_student_id(name, email):
    """Generate a unique student ID based on name and email."""
    import random
    import string
    if name and email:
        random_numbers = ''.join(random.choices(string.digits, k=4))
        random_letter = random.choice(string.ascii_uppercase)
        return random_numbers + random_letter
    return "N/A"
