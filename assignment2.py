import streamlit as st
import pandas as pd
import folium
from io import StringIO
from streamlit_folium import st_folium
from utils.style2 import set_page_style
from Record.google_sheet import fetch_student_record, update_google_sheet


def show():
    # Apply the custom page style
    set_page_style()

    st.title("Assignment 2: Real-Time Earthquake Analysis and Visualization")

    # Step 1: Validate Student ID
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Student ID")
        validate_button = st.form_submit_button("Validate")

        if validate_button:
            record = fetch_student_record(student_id)
            if record:
                st.success(f"Welcome back, {record['name']}! You are authorized to proceed with Assignment 2.")
            else:
                st.error("Invalid Student ID. Please check your ID and try again.")
                st.stop()

    # Step 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        In this assignment, you will fetch and analyze earthquake data using the USGS Earthquake API, filter the data, and create visualizations.

        **Tasks:**
        1. Fetch earthquake data for January 2nd, 2025, to January 9th, 2025.
        2. Filter earthquakes with a magnitude > 4.0.
        3. Create an interactive map with markers (color-coded by magnitude) and popups for details.
        4. Generate a bar chart of earthquake frequency by magnitude range.
        5. Produce a summary CSV with:
           - Total earthquakes > 4.0.
           - Average, max, and min magnitudes.
           - Count of earthquakes in magnitude ranges.

        **Expected Outputs:**
        - A map with earthquake locations.
        - A bar chart (`.png`) visualizing earthquake frequencies.
        - A CSV text summary of statistics.
        """)

    with tab2:
        st.markdown("""
        ### Grading Breakdown
        Your grade will be based on the following:
        - **API Integration (20 points)**: Successfully fetch data from the USGS API.
        - **Data Filtering (20 points)**: Correctly filter earthquakes with a magnitude > 4.0.
        - **Map Visualization (30 points)**: Create a map with markers, color-coded by magnitude, and popups.
        - **Bar Chart (20 points)**: Generate a bar chart of earthquake frequencies.
        - **Summary Statistics (10 points)**: Produce an accurate CSV with statistics.
        """)

    # Step 3: Submit and Run Code
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("Paste Your Python Code Here", height=300)

    # Run Code Button
    run_button = st.button("Run Code", key="run_code")
    if run_button and code_input:
        try:
            # Redirect stdout to capture print statements
            captured_output = StringIO()
            import sys
            sys.stdout = captured_output

            # Execute user-provided code in a controlled environment
            local_context = {}
            exec(code_input, {}, local_context)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Display captured outputs
            st.markdown("### Outputs")
            st.text(captured_output.getvalue())

            # Display Map
            map_object = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
            if map_object:
                st.markdown("#### Map Output")
                st_folium(map_object, width=700, height=500)

            # Display Bar Chart
            if "earthquake_chart.png" in local_context:
                st.markdown("#### Bar Chart Output")
                st.image("earthquake_chart.png")

            # Display CSV Summary
            summary_csv = local_context.get("summary_csv")
            if summary_csv:
                st.markdown("#### Summary Statistics")
                st.dataframe(pd.read_csv(StringIO(summary_csv)))

        except Exception as e:
            st.error(f"Error occurred while running your code: {e}")

    # Submit Button
    submit_button = st.button("Submit Assignment", key="submit_assignment")
    if submit_button:
        if not code_input:
            st.error("Please paste your code and run it before submitting.")
        elif record:
            from grades.grade2 import grade_assignment

            # Grade the assignment
            grade = grade_assignment(code_input)
            update_google_sheet(record["name"], record["email"], student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Unable to validate your submission. Please try again.")
