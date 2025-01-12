import streamlit as st
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet
import traceback
import folium
import pandas as pd
import os
import re

# Apply our custom styling (light blue background, etc.)
set_page_style()

def find_all_folium_maps(local_context):
    """
    Return a list of (var_name, var_value) for all folium.Map objects in local_context.
    """
    results = []
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            results.append((var_name, var_value))
    return results

def find_all_summaries(local_context):
    """
    Return a list of (var_name, string_value) for all string variables 
    containing 'summary' (case-insensitive) in local_context.
    """
    results = []
    for var_name, var_value in local_context.items():
        if isinstance(var_value, str) and re.search(r"summary", var_value, re.IGNORECASE):
            results.append((var_name, var_value))
    return results

def show():
    st.title("Assignment 2: Real-Time Earthquake Data Analysis")

    # Input field for the Student ID (must match an existing ID in the Google Sheet)
    student_id = st.text_input("Enter Your Student ID")

    # Tabs for Assignment Details and Grading Details
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        **Objective**  
        In this assignment, you will write a Python script that:
        - Fetches real-time earthquake data from the USGS Earthquake API.
        - Processes the data to filter earthquakes with a magnitude > 4.0.
        - Displays an interactive Folium map with color-coded markers.
        - Generates a bar chart as a PNG.
        - Produces a text summary of the key statistics.

        **Key Requirements**  
        1. Use the USGS Earthquake API for 2025-01-02 to 2025-01-09.
        2. Filter magnitude > 4.0.
        3. Map color-coded by magnitude:
           - Green for 4.0–5.0
           - Yellow for 5.0–5.5
           - Red for 5.5+
        4. Bar chart of earthquake frequency (saved as .png).
        5. Text summary (include average, max, min magnitudes, total count, etc.).
        """)

    with tab2:
        st.markdown("""
        **Grading Breakdown**  

        1. **Library Imports (10 Points)**  
           - folium, matplotlib/seaborn, requests/urllib, pandas, etc.
        2. **Code Quality (20 Points)**  
        3. **Fetching Data from the API (10 Points)**  
        4. **Filtering Earthquakes (10 Points)**  
        5. **Map Visualization (20 Points)**  
        6. **Bar Chart (15 Points)**  
        7. **Text Summary (15 Points)**  
        8. **Overall Execution (10 Points)**  
        """)

    # A text area for the user to paste their code
    code_input = st.text_area("Paste your code below", height=300)

    # Buttons for "Run" and "Submit"
    run_button = st.button("Run")
    submit_button = st.button("Submit")

    # 1) When the user clicks "Run", we exec their code
    if run_button and code_input:
        try:
            # Run the code in an isolated local context
            local_context = {}
            exec(code_input, {}, local_context)

            # (A) Detect all Folium maps
            all_maps = find_all_folium_maps(local_context)
            if all_maps:
                st.success(f"Detected {len(all_maps)} folium map object(s)!")
                for var_name, map_obj in all_maps:
                    st.markdown(f"**Map variable:** `{var_name}`")
                    st.components.v1.html(map_obj._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the code output.")

            # (B) Detect any PNG files in the working directory
            png_files = [f for f in os.listdir('.') if f.lower().endswith('.png')]
            if png_files:
                st.success(f"Detected {len(png_files)} PNG file(s).")
                for png_file in png_files:
                    st.markdown(f"**Displaying:** `{png_file}`")
                    st.image(png_file)
            else:
                st.warning("No PNG files found in the code output.")

            # (C) Detect any string variable containing 'summary' (case-insensitive)
            all_summaries = find_all_summaries(local_context)
            if all_summaries:
                st.success(f"Detected {len(all_summaries)} string variable(s) that contain 'summary'.")
                for var_name, text_val in all_summaries:
                    st.markdown(f"**Summary Variable:** `{var_name}`")
                    st.text(text_val)
            else:
                st.warning("No text summary found in the code output. "
                           "Try storing it in a string variable containing the word 'summary'.")

        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())

    # 2) When the user clicks "Submit", we run the grading and update Google Sheets
    if submit_button and code_input:
        if student_id:
            grade = grade_assignment(code_input)
            update_google_sheet("", "", student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please enter a valid Student ID before submitting.")
