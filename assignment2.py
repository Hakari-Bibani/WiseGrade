# assignment2.py
import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys


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
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:  # Verify student ID logic (placeholder)
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

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
        """)

    # Section 3: Code Submission and Output
    st.header("Step 3: Submit Your Code")
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

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
            st.markdown("### 📜 Captured Output")
            st.text(st.session_state["captured_output"])

        if st.session_state["map_object"]:
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["bar_chart"]:
            st.markdown("### 📊 Bar Chart Output")
            st.pyplot(st.session_state["bar_chart"])

        if st.session_state["dataframe_object"] is not None:
            st.markdown("### 📑 Data Summary")
            st.dataframe(st.session_state["dataframe_object"])

    if submit_button:
        if st.session_state.get("run_success", False):
            st.success("Code submitted successfully! Your outputs have been recorded.")
            # Save submission logic here (e.g., Google Sheets or database)
        else:
            st.error("Please run your code successfully before submitting.")
