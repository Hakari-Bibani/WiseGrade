import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import folium
from streamlit_folium import st_folium
import traceback
import sys
from io import StringIO
from utils.style2 import set_page_style
from Record.google_sheet import fetch_student_record, update_google_sheet

def show():
    # Apply the custom page style
    st.markdown(
        """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                color: #333;
            }
            .stButton > button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .stButton > button:hover {
                background-color: #45a049;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
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
    # Section 1: Student ID Form
    # Apply custom page style
    set_page_style()
    st.title("Assignment 2: Real-Time Earthquake Analysis and Visualization")
    # Section 1: Validate Student ID
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")
        student_id = st.text_input("Student ID")
        validate_button = st.form_submit_button("Validate")

        if submit_id_button:
            if student_id:  # Verify student ID logic (placeholder)
                st.success(f"Student ID {student_id} verified. You may proceed.")
        if validate_button:
            record = fetch_student_record(student_id)
            if record:
                st.success(f"Welcome back, {record['name']}! You are authorized to proceed with Assignment 2.")
            else:
                st.error("Please provide a valid Student ID.")
                st.error("Invalid Student ID. Please check your ID and try again.")
                st.stop()

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
@@ -69,94 +33,88 @@ def show():
    with tab1:
        st.markdown("""
        ### Objective
        Write a Python script that fetches real-time earthquake data from the USGS Earthquake API, filters earthquakes with a magnitude greater than 4.0, and visualizes the data on a map and as a bar chart.
        In this assignment, you will analyze real-time earthquake data using the USGS Earthquake API and produce visualizations and summaries.
        
        **Tasks:**
        - Fetch earthquake data for the date range January 2nd, 2025, to January 9th, 2025.
        - Filter data for earthquakes with a magnitude greater than 4.0.
        - Visualize the filtered data on a map with markers and popups.
        - Create a bar chart of earthquake frequencies by magnitude range.
        - Generate a summary CSV with key statistics.
        Use libraries: `folium`, `matplotlib`, `pandas`, and `requests`.
        **Expected Outputs:**
        - A map showing earthquake locations.
        - A bar chart (`.png`) visualizing earthquake frequency by magnitude range.
        - A CSV text summary of key statistics.
        """)

    with tab2:
        st.markdown("""
        ### Grading Details
        **1. Code Structure and Execution (40 points)**
        - Library imports and correct API usage.
        - Code runs without errors.
        **2. Map Visualization (30 points)**
        - Markers color-coded by magnitude range.
        - Popups display earthquake information.
        **3. Bar Chart Visualization (20 points)**
        - Correct bar chart representation of earthquake counts by magnitude.
        **4. Text Summary (10 points)**
        - Correct calculation of statistics: total earthquakes, average, maximum, and minimum magnitudes.
        Your grade will be based on the following criteria:
        - **API Integration (20 points)**: Successfully fetch data from the USGS API.
        - **Data Filtering (20 points)**: Correctly filter earthquakes with a magnitude > 4.0.
        - **Map Visualization (30 points)**: Create a map with colored markers and popups for additional info.
        - **Bar Chart (20 points)**: Generate a bar chart visualizing earthquake frequencies.
        - **Summary Statistics (10 points)**: Produce an accurate CSV summary.
        """)

    # Section 3: Code Submission and Output
    st.header("Step 3: Submit Your Code")
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)
    run_button = st.button("Run Code", key="run_code_button")
    submit_button = st.button("Submit Code", key="submit_code_button")
    # Section 3: Submit and Run Code
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("📝 Paste Your Python Code Here", height=300)

    # Run Code Button
    run_button = st.button("Run Code")
    if run_button and code_input:
        st.session_state["run_success"] = False
        st.session_state["captured_output"] = ""
        try:
            # Redirect stdout to capture output
            # Redirect stdout
            captured_output = StringIO()
            import sys
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
            # Execute code
            local_context = {}
            exec(code_input, {}, local_context)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Process outputs
            st.session_state["captured_output"] = captured_output.getvalue()
            st.session_state["map_object"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, folium.Map)), None)
            st.session_state["dataframe_object"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, pd.DataFrame)), None)
            st.session_state["bar_chart"] = plt.gcf() if plt.get_fignums() else None
            # Capture outputs
            st.markdown("### Outputs:")
            st.text(captured_output.getvalue())

            st.session_state["run_success"] = True
            # Map Output
            map_object = next((v for v in local_context.values() if isinstance(v, folium.Map)), None)
            if map_object:
                st.markdown("#### Map Output:")
                st_folium(map_object, width=700, height=500)

        except Exception as e:
            sys.stdout = sys.__stdout__
            st.error(f"An error occurred while running your code: {e}")
            st.error(traceback.format_exc())
    # Display Outputs
    if st.session_state["run_success"]:
        if st.session_state["captured_output"]:
            st.markdown("### 📜 Captured Output")
            st.text(st.session_state["captured_output"])
            # Bar Chart Output
            if "earthquake_chart.png" in local_context:
                st.markdown("#### Bar Chart Output:")
                st.image("earthquake_chart.png")

        if st.session_state["map_object"]:
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)
            # CSV Output
            summary_csv = local_context.get("summary_csv")
            if summary_csv:
                st.markdown("#### Summary Statistics:")
                st.dataframe(pd.read_csv(StringIO(summary_csv)))

        if st.session_state["bar_chart"]:
            st.markdown("### 📊 Bar Chart Output")
            st.pyplot(st.session_state["bar_chart"])
        if st.session_state["dataframe_object"] is not None:
            st.markdown("### 📑 Data Summary")
            st.dataframe(st.session_state["dataframe_object"])
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Submit Code Button
    submit_button = st.button("Submit Assignment")
    if submit_button:
        if st.session_state.get("run_success", False):
            st.success("Code submitted successfully! Your outputs have been recorded.")
        if not code_input:
            st.error("Please paste your code and run it before submitting.")
        elif record:
            from grades.grade2 import grade_assignment
            grade = grade_assignment(code_input)
            update_google_sheet(record['name'], record['email'], student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please run your code successfully before submitting.")
            st.error("Unable to validate your submission. Please try again.")
