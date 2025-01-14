import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys
from Record.google_sheet import get_student_ids, update_google_sheet
from grades.grade2 import grade_assignment2

def show():
    # Apply the custom page style
@@ -51,21 +50,17 @@

    st.title("Assignment 2: Earthquake Data Analysis")

    # Fetch valid student IDs from Google Sheet
    valid_student_ids = get_student_ids()
    # Section 1: Student ID Form
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id in valid_student_ids:
            if student_id:  # Verify student ID logic (placeholder)
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Invalid Student ID. Please ensure you are using the ID saved in Assignment 1.")
                return
                st.error("Please provide a valid Student ID.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
@@ -105,7 +100,7 @@

    # Section 3: Code Submission and Output
    st.header("Step 3: Submit Your Code")
    code_input = st.text_area("**\U0001F4DD Paste Your Code Here**", height=300)
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

    run_button = st.button("Run Code", key="run_code_button")
    submit_button = st.button("Submit Code", key="submit_code_button")
@@ -152,32 +147,24 @@
    # Display Outputs
    if st.session_state["run_success"]:
        if st.session_state["captured_output"]:
            st.markdown("### \U0001F4DA Captured Output")
            st.markdown("### 📜 Captured Output")
            st.text(st.session_state["captured_output"])

        if st.session_state["map_object"]:
            st.markdown("### \U0001F5FA Map Output")
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["bar_chart"]:
            st.markdown("### \U0001F4C8 Bar Chart Output")
            st.markdown("### 📊 Bar Chart Output")
            st.pyplot(st.session_state["bar_chart"])

        if st.session_state["dataframe_object"] is not None:
            st.markdown("### \U0001F4CA Data Summary")
            st.markdown("### 📑 Data Summary")
            st.dataframe(st.session_state["dataframe_object"])

    if submit_button:
        if st.session_state.get("run_success", False):
            # Grade the assignment
            grade = grade_assignment2(code_input)
            st.success(f"Submission successful! Your grade: {grade}/100")
            # Save the grade to Google Sheets
            update_google_sheet(
                student_id=student_id,
                assignment_name="assignment_2",
                grade=grade
            )
            st.success("Code submitted successfully! Your outputs have been recorded.")
            # Save submission logic here (e.g., Google Sheets or database)
        else:
            st.error("Please run your code successfully before submitting.")
