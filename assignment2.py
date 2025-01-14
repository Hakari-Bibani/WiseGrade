import streamlit as st
import folium
import pandas as pd
@@ -6,13 +7,35 @@
from streamlit_folium import st_folium
import traceback
import sys
from Record.google_sheet import get_student_ids, update_google_sheet
from grades.grade2 import grade_assignment2
from Record.google_sheet import get_student_data, update_google_sheet
from utils.style2 import set_page_style  # Import the style function

def show():
    # Apply the custom page style
    set_page_style()  # Apply the styles from style2.py
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
@@ -28,21 +51,21 @@ def show():

    st.title("Assignment 2: Earthquake Data Analysis")

    # Fetch valid student IDs from Google Sheet
    valid_student_ids = get_student_ids()
    # Section 1: Student ID Form
    st.header("Step 1: Enter Your Student ID")
    valid_student_id = False
    student_data = get_student_data()  # Fetch student data from Google Sheet
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id in student_data:
            if student_id in valid_student_ids:
                st.success(f"Student ID {student_id} verified. You may proceed.")
                valid_student_id = True
            else:
                st.error("Invalid Student ID. Please enter a valid ID from Assignment 1.")
                st.error("Invalid Student ID. Please ensure you are using the ID saved in Assignment 1.")
                return

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
@@ -145,17 +168,16 @@ def show():
            st.dataframe(st.session_state["dataframe_object"])

    if submit_button:
        if st.session_state.get("run_success", False) and valid_student_id:
            # Grade the code
        if st.session_state.get("run_success", False):
            # Grade the assignment
            grade = grade_assignment2(code_input)
            st.success(f"Submission successful! Your grade: {grade}/100")

            # Update Google Sheet
            # Save the grade to Google Sheets
            update_google_sheet(
                student_id=student_id,
                grade=grade,
                assignment="assignment_2"
                assignment_name="assignment_2",
                grade=grade
            )
            st.success(f"Code submitted successfully! Your grade: {grade}/100.")
        else:
            st.error("Please ensure your Student ID is verified and the code runs successfully before submitting.")
            st.error("Please run your code successfully before submitting.")
