import streamlit as st
import traceback
import io
import sys
import os

from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    # Apply custom styling (light blue background for code box, etc.)
    set_page_style()

    # Page title
    st.title("Assignment 2: Real-Time Earthquake Data Analysis")

    # Student ID field (must match an existing ID from Assignment 1 in Google Sheets)
    student_id = st.text_input("Enter Your Student ID")

    # Two tabs: Assignment Details & Grading Details
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        **Objective**  
        In this assignment, you will write a Python script that fetches real-time earthquake data from the USGS Earthquake API, processes the data to filter earthquakes with a magnitude greater than 4.0, and plots the earthquake locations on a map. Additionally, you will calculate the number of earthquakes in different magnitude ranges and present the results visually.

        **API Reference**  
        The USGS Earthquake API can be accessed at:  
        [https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=YYYY-MM-DD&endtime=YYYY-MM-DD](https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=YYYY-MM-DD&endtime=YYYY-MM-DD)

        **Task Requirements**  
        - Use the USGS Earthquake API to fetch data for the date range **January 2nd, 2025, to January 9th, 2025**.
        - Filter to include only earthquakes with **magnitude > 4.0**.
        - Create an interactive map showing the filtered earthquakes.
          - Markers color-coded by magnitude range:
            - Green for 4.0-5.0  
            - Yellow for 5.0-5.5  
            - Red for 5.5+  
        - Add popups displaying magnitude, location, and time (in readable format).
        - Generate a **bar chart** illustrating earthquake frequency by magnitude range:
          - 4.0-4.5, 4.5-5.0, and greater than 5.0
        - Generate a **text summary** (and save as CSV) including:
          1. Total number of earthquakes (mag > 4.0)
          2. Average, maximum, and minimum magnitudes (rounded to 2 decimals)
          3. Number of earthquakes in each magnitude range

        **Python Libraries to Use**  
        - `requests` or `urllib` for the API calls  
        - `pandas` for data processing  
        - `folium` for map visualization  
        - `matplotlib` or `seaborn` for bar chart  

        **Expected Output**  
        1. An interactive map of earthquake locations (save as `earthquake_map.html`)  
        2. A bar chart of the earthquake frequency by magnitude range (save as `earthquake_frequency.png`)  
        3. A text summary (also printed, plus optional CSV)  
        """)

    with tab2:
        st.markdown("""
        **Grading Breakdown**  

        1. **Library Imports (10 Points)**  
           - folium, matplotlib/seaborn, requests/urllib, pandas (8 points)  
           - Proper import organization/no unused libs (2)  

        2. **Code Quality (20 Points)**  
           - Variable Naming (5), Spacing (5), Comments (5), Organization (5)  

        3. **Fetching Data from API (10 Points)**  
           - Correct URL/dates, successful retrieval, error handling  

        4. **Filtering Earthquakes (10 Points)**  
           - Magnitude > 4.0, extract lat/lon/mag/time  

        5. **Map Visualization (20 Points)**  
           - Display map, color-coded markers, popups with details  

        6. **Bar Chart (15 Points)**  
           - Show bar chart for 4.0-4.5, 4.5-5.0, 5.0+  

        7. **Text Summary (15 Points)**  
           - Total count, average/max/min mag, count by range, CSV output  

        8. **Overall Execution (10 Points)**  
           - Runs without errors, complete outputs  
        """)

    # Text area (light blue styled by style2.py) for user to paste code
    code_input = st.text_area("Paste your code below:", height=300)

    # Buttons for run & submit
    run_button = st.button("Run")
    submit_button = st.button("Submit")

    # --- RUN the user's code ---
    if run_button and code_input:
        # 1) Clean up any old artifact files from previous runs
        if os.path.exists("earthquake_map.html"):
            os.remove("earthquake_map.html")
        if os.path.exists("earthquake_frequency.png"):
            os.remove("earthquake_frequency.png")

        # 2) Capture stdout so we can show printed text summary
        buffer = io.StringIO()
        original_stdout = sys.stdout

        try:
            sys.stdout = buffer
            # Execute user code in a fresh local context
            exec(code_input, {}, {})
        except Exception:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())
        finally:
            sys.stdout = original_stdout

        # 3) Retrieve the output text (summary, etc.)
        printed_output = buffer.getvalue()

        # Display what the user's code printed
        if printed_output.strip():
            st.markdown("### Printed Summary/Output")
            st.text(printed_output)
        else:
            st.warning("No text summary found in the output.")

        # 4) Check if the student's code generated an HTML map
        if os.path.exists("earthquake_map.html"):
            st.markdown("### Generated Earthquake Map")
            with open("earthquake_map.html", "r", encoding="utf-8") as file:
                html_map = file.read()
            st.components.v1.html(html_map, height=600)
        else:
            st.warning("No Folium map file (earthquake_map.html) found.")

        # 5) Check if the student's code saved a bar chart
        if os.path.exists("earthquake_frequency.png"):
            st.markdown("### Generated Bar Chart")
            st.image("earthquake_frequency.png")
        else:
            st.warning("No bar chart file (earthquake_frequency.png) found.")

    # --- SUBMIT for Grading ---
    if submit_button and code_input:
        if student_id:
            grade = grade_assignment(code_input)
            update_google_sheet("", "", student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please enter a valid Student ID before submitting.")
