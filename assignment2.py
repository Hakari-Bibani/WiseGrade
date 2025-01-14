import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from io import StringIO
import sys
from utils.style2 import set_page_style
from Record.google_sheet import fetch_student_record, update_google_sheet

def show():
    # Apply custom page style
    set_page_style()

    st.title("Assignment 2: Real-Time Earthquake Analysis and Visualization")

    # Initialize session state variables
    if "student_id" not in st.session_state:
        st.session_state["student_id"] = None
    if "record" not in st.session_state:
        st.session_state["record"] = None
    if "code_output" not in st.session_state:
        st.session_state["code_output"] = ""
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None
    if "summary_csv" not in st.session_state:
        st.session_state["summary_csv"] = None

    # Section 1: Validate Student ID
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Student ID", key="student_id_input")
        validate_button = st.form_submit_button("Validate")

        if validate_button:
            if student_id:
                record = fetch_student_record(student_id)
                if record:
                    st.session_state["student_id"] = student_id
                    st.session_state["record"] = record
                    st.success(f"Student ID {student_id} validated. Welcome, {record['name']}!")
                else:
                    st.error("Invalid Student ID. Please check your ID and try again.")
                    st.stop()
            else:
                st.error("Please enter a valid Student ID.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        In this assignment, you will fetch and analyze earthquake data using the USGS Earthquake API, filter the data, and create visualizations.
        Use libraries: `folium`, `matplotlib`, `pandas`, and `requests`.
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

    # Section 3: Submit and Run Code
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("Paste Your Python Code Here", height=300, key="code_input")

    # Run Code Button
    run_button = st.button("Run Code", key="run_code")
    if run_button and code_input:
        try:
            # Redirect stdout to capture print statements
            captured_output = StringIO()
            sys.stdout = captured_output

            # Execute user-provided code in a controlled environment
            local_context = {}
            exec(code_input, {}, local_context)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Capture outputs
            st.session_state["code_output"] = captured_output.getvalue()
            st.session_state["map_object"] = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
            st.session_state["bar_chart"] = local_context.get("earthquake_chart.png")
            st.session_state["summary_csv"] = local_context.get("summary_csv")

            st.success("Code executed successfully!")

        except Exception as e:
            st.error(f"An error occurred while running your code: {e}")
            st.session_state["code_output"] = str(e)

    # Display Outputs
    if st.session_state["code_output"]:
        st.markdown("### Outputs")
        st.text(st.session_state["code_output"])

    if st.session_state["map_object"]:
        st.markdown("#### Map Output")
        st_folium(st.session_state["map_object"], width=700, height=500)

    if st.session_state["bar_chart"]:
        st.markdown("#### Bar Chart Output")
        st.image(st.session_state["bar_chart"])

    if st.session_state["summary_csv"]:
        st.markdown("#### Summary Statistics")
        st.dataframe(pd.read_csv(StringIO(st.session_state["summary_csv"])))

    # Section 4: Submit Assignment
    st.header("Step 4: Submit Assignment")
    submit_button = st.button("Submit Assignment", key="submit_assignment")
    if submit_button:
        if not code_input:
            st.error("Please paste your code and run it before submitting.")
        elif st.session_state["record"]:
            from grades.grade2 import grade_assignment

            # Grade the assignment
            grade = grade_assignment(code_input)
            update_google_sheet(
                st.session_state["record"]["name"],
                st.session_state["record"]["email"],
                st.session_state["student_id"],
                grade,
                "assignment_2"
            )
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Unable to validate your submission. Please try again.")

if __name__ == "__main__":
    show()
