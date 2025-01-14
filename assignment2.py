import streamlit as st
import traceback
import sys
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium


def show():
    # Apply custom page style
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
        unsafe_allow_html=True,
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

    # Step 1: Enter Student ID
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

    # Step 2: Assignment Instructions
    st.header("Step 2: Review Assignment Details")
    st.markdown("""
    ### Objective
    Write a Python script that:
    - Fetches real-time earthquake data from the USGS Earthquake API for January 2-9, 2025.
    - Filters earthquakes with a magnitude greater than 4.0.
    - Visualizes the data on a map and as a bar chart.
    - Provides a CSV summary of key metrics.

    ### Output Requirements
    1. A map of earthquake locations (color-coded markers).
    2. A bar chart of earthquake counts by magnitude range.
    3. A CSV summary with total count, average, min, and max magnitudes.
    """)

    # Step 3: Code Editor
    st.header("Step 3: Write and Run Your Code")
    code = st.text_area("Paste your Python code here", height=300)

    # Run Code Button
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
            # Define a controlled environment to execute the user code
            user_namespace = {}

            # Execute the user's code
            exec(code, {"folium": folium, "pd": pd, "plt": plt, "st": st}, user_namespace)

            # Capture results from user-defined variables
            st.session_state["run_success"] = True
            st.session_state["captured_output"] = new_stdout.getvalue()

            # Look for specific objects in user namespace
            if "map_object" in user_namespace:
                st.session_state["map_object"] = user_namespace["map_object"]
            if "dataframe_object" in user_namespace:
                st.session_state["dataframe_object"] = user_namespace["dataframe_object"]
            if "bar_chart" in user_namespace:
                st.session_state["bar_chart"] = user_namespace["bar_chart"]

            st.success("Code executed successfully!")
        except Exception as e:
            st.error("An error occurred during execution. Please review your code.")
            st.session_state["captured_output"] = traceback.format_exc()
        finally:
            sys.stdout = old_stdout

    # Display Outputs
    st.header("Step 4: Visualize Your Outputs")

    # Text Output
    st.markdown("### Text Output")
    st.text_area("Captured Output", st.session_state["captured_output"], height=150)

    # Map Output
    if st.session_state.get("map_object"):
        st.markdown("### Interactive Map")
        st_folium(st.session_state["map_object"], width=700, height=500)

    # DataFrame Output
    if st.session_state.get("dataframe_object") is not None:
        st.markdown("### Data Summary (DataFrame)")
        st.dataframe(st.session_state["dataframe_object"])

    # Bar Chart Output
    if st.session_state.get("bar_chart"):
        st.markdown("### Bar Chart Visualization")
        st.pyplot(st.session_state["bar_chart"])

    # Step 5: Submit Assignment
    st.header("Step 5: Submit Your Assignment")
    if st.button("Submit Assignment"):
        if st.session_state.get("run_success", False):
            st.success("Assignment submitted successfully!")
            # Placeholder for submission logic
        else:
            st.error("Please run your code successfully before submitting.")
