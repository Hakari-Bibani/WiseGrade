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
@@ -165,6 +158,5 @@
    if submit_button:
        if st.session_state.get("run_success", False):
            st.success("Code submitted successfully! Your outputs have been recorded.")
            # Save submission logic here (e.g., Google Sheets or database)
        else:
            st.error("Please run your code successfully before submitting.")
