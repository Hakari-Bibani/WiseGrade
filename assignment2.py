import streamlit as st
import folium
import pandas as pd
from io import StringIO
from streamlit_folium import st_folium
from utils.style2 import set_page_style
from Record.google_sheet import fetch_student_record, update_google_sheet

def show():
    # Apply custom styles
    set_page_style()

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
    run_button = st.button("Run Code", key="run_code")
    if run_button and code_input:
        try:
            # Redirect stdout to capture print statements
            captured_output = StringIO()
            import sys
            sys.stdout = captured_output

            # Execute the user code
            local_context = {}
            exec(code_input, {}, local_context)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Display Captured Outputs
            st.markdown("### Outputs:")
            if captured_output.getvalue():
                st.text(captured_output.getvalue())
            else:
                st.write("No console output was captured.")

            # Display Map Output
            map_object = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
            if map_object:
                st.markdown("#### Map Output:")
                st_folium(map_object, width=700, height=500)

            # Display Bar Chart
            if "earthquake_chart.png" in local_context:
                st.markdown("#### Bar Chart Output:")
                st.image("earthquake_chart.png")

            # Display CSV Summary
            summary_csv = local_context.get("summary_csv")
            if summary_csv:
                st.markdown("#### Summary Statistics:")
                st.dataframe(pd.read_csv(StringIO(summary_csv)))

        except Exception as e:
            st.error(f"Error while running your code: {e}")

    # Submit Button
    submit_button = st.button("Submit Assignment", key="submit_assignment")
    if submit_button:
        if not code_input:
            st.error("Please paste and run your code before submitting.")
        else:
            from grades.grade2 import grade_assignment

            # Grade the assignment
            grade = grade_assignment(code_input)
            update_google_sheet(record["name"], record["email"], student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
