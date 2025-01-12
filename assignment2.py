import streamlit as st
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet
import traceback
import folium
import pandas as pd
import os
import re

# Apply custom styling (light blue code box, etc.)
set_page_style()

def find_all_folium_maps(local_context):
    """
    Return a list of (variable_name, variable_value) for all folium.Map objects found.
    """
    results = []
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            results.append((var_name, var_value))
    return results

def find_all_summaries(local_context):
    """
    Return a list of (variable_name, string_value) for all string variables 
    containing 'summary' (case-insensitive).
    """
    results = []
    for var_name, var_value in local_context.items():
        if isinstance(var_value, str) and re.search(r"summary", var_value, re.IGNORECASE):
            results.append((var_name, var_value))
    return results

def show():
    st.title("Assignment 2: Real-Time Earthquake Data Analysis")

    # Student ID field (this must match an existing ID from Assignment 1 in the Google Sheet)
    student_id = st.text_input("Enter Your Student ID")

    # Create tabs for the Assignment and Grading details
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        **Objective**  
        In this assignment, you will write a Python script that fetches real-time earthquake data from the USGS Earthquake API, 
        processes the data to filter earthquakes with a magnitude greater than 4.0, 
        and plots the earthquake locations on a map. 
        Additionally, you will calculate the number of earthquakes in different magnitude ranges 
        and present the results visually.

        **Key Points**  
        - Use the USGS Earthquake API with the date range: 2025-01-02 to 2025-01-09.
        - Filter earthquakes with magnitude > 4.0.
        - Display an interactive Folium map with colored markers (Green, Yellow, Red based on magnitude range).
        - Generate a bar chart (matplotlib/seaborn) and save it as a PNG.
        - Provide a text summary of results.
        """)

    with tab2:
        st.markdown("""
        **Grading Breakdown**  

        1. **Library Imports (10 Points)**  
           - folium, matplotlib/seaborn, requests/urllib, pandas  
        2. **Code Quality (20 Points)**  
        3. **Fetching Data from the API (10 Points)**  
        4. **Filtering Earthquakes (10 Points)**  
        5. **Map Visualization (20 Points)**  
        6. **Bar Chart (15 Points)**  
        7. **Text Summary (15 Points)**  
        8. **Overall Execution (10 Points)**  
        """)

    # Code submission area (light blue background in style2.py)
    code_input = st.text_area("Paste your code below", height=300)

    # Buttons for run and submit
    run_button = st.button("Run")
    submit_button = st.button("Submit")

    # Run the user code
    if run_button and code_input:
        try:
            # Run code in an isolated local context
            local_context = {}
            exec(code_input, {}, local_context)

            # 1. Detect all Folium maps
            all_maps = find_all_folium_maps(local_context)
            if all_maps:
                st.success(f"Detected {len(all_maps)} folium Map object(s)!")
                for var_name, map_obj in all_maps:
                    st.markdown(f"### Map variable: `{var_name}`")
                    st.components.v1.html(map_obj._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the code output.")

            # 2. Detect any PNG file(s) in the current directory
            png_files = [f for f in os.listdir('.') if f.lower().endswith('.png')]
            if png_files:
                st.success(f"Detected {len(png_files)} PNG file(s).")
                for png_file in png_files:
                    st.markdown(f"### Displaying: {png_file}")
                    st.image(png_file)
            else:
                st.warning("No PNG files found in the code output.")

            # 3. Detect any summaries
            all_summaries = find_all_summaries(local_context)
            if all_summaries:
                st.success(f"Detected {len(all_summaries)} string variable(s) containing 'summary'.")
                for var_name, summary_text in all_summaries:
                    st.markdown(f"### Potential Summary Variable: `{var_name}`")
                    st.text(summary_text)
            else:
                st.warning("No text summary found in the code output. "
                           "Hint: store your summary in a variable containing the word 'summary'.")

        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())

    # Submit and grade
    if submit_button and code_input:
        if student_id:
            grade = grade_assignment(code_input)
            update_google_sheet("", "", student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please enter a valid Student ID before submitting.")
