import streamlit as st
import folium
import pandas as pd
@@ -9,33 +8,11 @@
import sys
from grades.grade2 import grade_assignment2
from Record.google_sheet import get_student_data, update_google_sheet
from utils.style2 import set_page_style  # Import the style function

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
    set_page_style()  # Apply the styles from style2.py

    # Initialize session state variables
    if "run_success" not in st.session_state:
@@ -51,27 +28,29 @@

    st.title("Assignment 2: Earthquake Data Analysis")

    st.title("Assignment 2: Earthquake Data Analysis")
    # Section 1: Student ID Form
    st.header("Step 1: Enter Your Student ID")
    valid_student_id = False
    student_data = get_student_data()  # Fetch student data from Google Sheet

    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id in student_data:
                st.success(f"Student ID {student_id} verified. You may proceed.")
                valid_student_id = True
            else:
                st.error("Invalid Student ID. Please enter a valid ID from Assignment 1.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        Write a Python script that fetches real-time earthquake data from the USGS Earthquake API, filters earthquakes with a magnitude greater than 4.0, and visualizes the data on a map and as a bar chart.
