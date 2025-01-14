# assignment2.py
import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys
from grades.grade2 import grade_assignment2
from Record.google_sheet import update_google_sheet, verify_student_id
from Record.google_sheet import get_student_data, update_google_sheet

def show():
    # Apply the custom page style
@@ -53,17 +53,19 @@

    # Section 1: Student ID Form
    st.header("Step 1: Enter Your Student ID")
    valid_student_id = False
    student_data = get_student_data()  # Fetch student data from Google Sheet
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if verify_student_id(student_id):  # Verify student ID using Google Sheets
            if student_id in student_data:
                st.success(f"Student ID {student_id} verified. You may proceed.")
                st.session_state["student_id_verified"] = True
                valid_student_id = True
            else:
                st.error("Invalid Student ID. Please provide a valid ID from Assignment 1.")
                st.session_state["student_id_verified"] = False
                st.error("Invalid Student ID. Please enter a valid ID from Assignment 1.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
@@ -166,10 +168,17 @@
            st.dataframe(st.session_state["dataframe_object"])

    if submit_button:
        if st.session_state.get("run_success", False) and st.session_state.get("student_id_verified", False):
            grade = grade_assignment2(code_input)  # Grade the assignment
            student_id = st.session_state.get("student_id")
            update_google_sheet(student_id, grade, "assignment_2")  # Save grade in Google Sheet
            st.success(f"Code submitted successfully! Your grade: {grade}/100")
        if st.session_state.get("run_success", False) and valid_student_id:
            # Grade the code
            grade = grade_assignment2(code_input)
            # Update Google Sheet
            update_google_sheet(
                student_id=student_id,
                grade=grade,
                assignment="assignment_2"
            )
            st.success(f"Code submitted successfully! Your grade: {grade}/100.")
        else:
            st.error("Please ensure your Student ID is verified and your code runs successfully before submitting.")
            st.error("Please ensure your Student ID is verified and the code runs successfully before submitting.")
