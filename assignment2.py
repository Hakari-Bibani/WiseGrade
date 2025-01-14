import streamlit as st
import folium
import pandas as pd
from io import StringIO
from streamlit_folium import st_folium
from utils.style2 import set_page_style
from Record.google_sheet import check_student_id, update_google_sheet


def show():
    # Apply custom page style
    set_page_style()

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "chart_image" not in st.session_state:
        st.session_state["chart_image"] = None
    if "text_summary" not in st.session_state:
        st.session_state["text_summary"] = ""

    st.title("Assignment 2: Earthquake Data Analysis and Visualization")

    # Section 1: Student ID Verification
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter your Student ID (from Assignment 1)", key="student_id_input")
        verify_id_button = st.form_submit_button("Verify Student ID")

        if verify_id_button:
            if student_id and check_student_id(student_id):
                st.success("Student ID verified successfully!")
                st.session_state["verified_student_id"] = student_id
            else:
                st.error("Invalid Student ID. Please enter a valid ID from Assignment 1.")

    # Ensure student ID is verified before proceeding
    if "verified_student_id" not in st.session_state:
        st.stop()

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        Write a Python script to fetch real-time earthquake data, filter it, and visualize it on a map and with a bar chart.

        **Steps:**
        - Fetch data using the USGS Earthquake API for the date range January 2nd, 2025, to January 9th, 2025.
        - Filter earthquakes with magnitude greater than 4.0.
        - Create a map with markers showing earthquake locations, colored by magnitude range.
        - Generate a bar chart showing earthquake frequencies in magnitude ranges.
        - Provide a summary of total earthquakes, statistics (min, max, average magnitude), and counts per range.
        """)

    with tab2:
        st.markdown("""
        ### Grading Criteria
        **1. Code Execution (30 points):**
        - Full points if the script executes without errors.

        **2. Map Visualization (30 points):**
        - Map generation (10 points).
        - Correct markers and coloring (10 points).
        - Popups for details (10 points).

        **3. Bar Chart and Summary (40 points):**
        - Accurate bar chart (20 points).
        - Correct statistical summary (20 points).
        """)

    # Section 3: Code Submission and Execution
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

    # Run Code Button
    run_button = st.button("Run Code", key="run_code_button")
    if run_button and code_input:
        st.session_state["run_success"] = False
        st.session_state["text_summary"] = ""
        try:
            # Redirect stdout to capture print statements
            captured_output = StringIO()
            import sys
            sys.stdout = captured_output

            # Execute the user's code
            local_context = {}
            exec(code_input, {}, local_context)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Capture outputs
            st.session_state["text_summary"] = captured_output.getvalue()
            st.session_state["map_object"] = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
            st.session_state["chart_image"] = next((obj for obj in local_context.values() if isinstance(obj, str) and obj.endswith(".png")), None)

            st.session_state["run_success"] = True
        except Exception as e:
            sys.stdout = sys.__stdout__
            st.error(f"An error occurred while running your code: {e}")

    # Display Outputs
    if st.session_state["run_success"]:
        st.markdown("### 📄 Captured Output")
        if st.session_state["text_summary"]:
            st.text(st.session_state["text_summary"])

        if st.session_state["map_object"]:
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["chart_image"]:
            st.markdown("### 📊 Bar Chart Output")
            st.image(st.session_state["chart_image"], caption="Bar Chart of Earthquake Frequencies")

    # Submit Code Button
    submit_button = st.button("Submit Code", key="submit_code_button")
    if submit_button:
        if not st.session_state.get("run_success", False):
            st.error("Please run your code successfully before submitting.")
        else:
            from grades.grade2 import grade_assignment

            grade = grade_assignment(code_input)
            update_google_sheet(st.session_state["verified_student_id"], grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
