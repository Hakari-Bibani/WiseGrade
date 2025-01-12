import streamlit as st
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet
import traceback
import folium
import pandas as pd

# Apply custom styling (light blue code box, etc.)
set_page_style()

def find_folium_map(local_context):
    """Search for a Folium map object in the local context."""
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            return var_value
    return None

def find_dataframe(local_context):
    """Search for a Pandas DataFrame (or similar) in the local context."""
    for var_name, var_value in local_context.items():
        if isinstance(var_value, pd.DataFrame):
            return var_value
    return None

def show():
    st.title("Assignment 2: Real-Time Earthquake Data Analysis")

    # Student ID field (this must match an existing ID from Assignment 1 in the Google Sheet)
    student_id = st.text_input("Enter Your Student ID")

    # Create tabs for the Assignment and Grading details
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
        1. An interactive map of earthquake locations  
        2. A bar chart of the earthquake frequency by magnitude range  
        3. A text summary (CSV) with required metrics  
        """)

    with tab2:
        st.markdown("""
        **Grading Breakdown**  

        1. **Library Imports (10 Points)**  
           - folium, matplotlib/seaborn, requests/urllib, pandas (8 points)  
           - Proper import organization and no unused libraries (2 points)  

        2. **Code Quality (20 Points)**  
           - Variable Naming (5)  
           - Spacing (5)  
           - Comments (5)  
           - Code Organization (5)  

        3. **Fetching Data from the API (10 Points)**  
           - Correct URL for date range (3)  
           - Successful data retrieval (3)  
           - Proper error handling (4)  

        4. **Filtering Earthquakes (10 Points)**  
           - Filter magnitude > 4.0 (5)  
           - Extract latitude, longitude, magnitude, time (5)  

        5. **Map Visualization (20 Points)**  
           - Display map (5)  
           - Color-coded markers:  
             - Green (4.0-5.0): 3  
             - Yellow (5.0-5.5): 3  
             - Red (5.5+): 3  
           - Popups for magnitude, lat/long, time (2 + 2 + 2)  

        6. **Bar Chart (15 Points)**  
           - Display bar chart (5)  
           - Magnitude ranges (4.0-4.5, 4.5-5.0, 5.0+) (3+3+3)  
           - Proper labeling (1)  

        7. **Text Summary (15 Points)**  
           - Total count of earthquakes (3)  
           - Average, max, min magnitude (3 each)  
           - Magnitude range counts (4.0-4.5, 4.5-5.0, 5.0+) (1 each)  
           - Must save as CSV (-5 if missing)  

        8. **Overall Execution (10 Points)**  
           - Runs without errors (5)  
           - All outputs correct and complete (5)  
        """)

    # Code submission area (light blue background in style2.py)
    code_input = st.text_area("Paste your code below", height=300)

    # Buttons for run and submit
    run_button = st.button("Run")
    submit_button = st.button("Submit")

    # Run the user code
    if run_button and code_input:
        try:
            local_context = {}
            exec(code_input, {}, local_context)

            # Try to find a folium map object
            map_object = find_folium_map(local_context)
            if map_object:
                st.success("Map generated successfully!")
                # Display map in Streamlit
                st.markdown("### 🗺️ Generated Map")
                st.components.v1.html(map_object._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the code output.")

            # Try to find a DataFrame object
            dataframe_object = find_dataframe(local_context)
            if dataframe_object is not None:
                st.markdown("### 📊 Earthquake Summary DataFrame")
                st.write(dataframe_object)
            else:
                st.warning("No DataFrame found in the code output.")

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
