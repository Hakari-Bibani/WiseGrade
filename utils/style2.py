import streamlit as st
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet
import traceback

# Set the page style
set_page_style()

def show():
    st.title("Assignment 2: Earthquake Data Analysis and Visualization")

    # Student ID Input
    student_id = st.text_input("Enter Your Student ID", key="student_id")

    # Tabs for assignment and grading details
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown(
            """
            ### Objective
            In this assignment, you will write a Python script that fetches real-time earthquake data from the USGS Earthquake API, processes the data to filter earthquakes with a magnitude greater than 4.0, and plots the earthquake locations on a map. Additionally, you will calculate the number of earthquakes in different magnitude ranges and present the results visually.

            ### Assignment Details
            - Use the API URL: [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=YYYY-MM-DD&endtime=YYYY-MM-DD)
            - Replace `YYYY-MM-DD` with the appropriate dates (January 2nd, 2025, to January 9th, 2025).

            #### Task Requirements
            1. Fetch earthquake data for the given date range.
            2. Filter data to include earthquakes with magnitude > 4.0.
            3. Create an interactive map with markers for earthquake locations:
                - Green: Magnitude 4-5
                - Yellow: Magnitude 5-5.5
                - Red: Magnitude > 5.5
            4. Add popups with earthquake details (magnitude, location, time).
            5. Generate a bar chart visualizing earthquake frequency by magnitude ranges:
                - 4.0-4.5, 4.5-5.0, >5.0.
            6. Generate a text summary with:
                - Total number of earthquakes with magnitude > 4.0.
                - Average, maximum, and minimum magnitudes.
                - Earthquake counts in each magnitude range.

            #### Expected Output
            - Interactive map
            - Bar chart
            - Text summary (CSV format)

            #### Python Libraries You Will Use
            - `folium` for the map.
            - `matplotlib` or `seaborn` for the bar chart.
            - `requests` or `urllib` for API calls.
            - `pandas` for data processing.
            """
        )

    with tab2:
        st.markdown(
            """
            ### Grading Criteria

            #### 1. Library Imports (10 Points)
            - folium for the map: 2 points
            - matplotlib or seaborn for the bar chart: 2 points
            - requests or urllib for API calls: 2 points

            #### 2. Data Processing and Filtering (20 Points)
            - Fetching and filtering earthquake data: 10 points
            - Correct data range: 10 points

            #### 3. Map Visualization (30 Points)
            - Markers with appropriate colors: 10 points
            - Popups with earthquake details: 10 points
            - Correct location plotting: 10 points

            #### 4. Bar Chart Visualization (20 Points)
            - Correct frequency ranges: 10 points
            - Visual clarity: 10 points

            #### 5. Text Summary (20 Points)
            - Correct statistics: 10 points
            - Formatting and clarity: 10 points

            """
        )

    # Code Submission Area
    st.markdown("**📝 Paste Your Code Below**")
    code_input = st.text_area("Code Area", height=200, key="code_input", help="Paste your Python code here.")

    # File Upload Areas
    st.markdown("**📤 Upload Your Outputs**")
    map_file = st.file_uploader("Upload your map HTML file", type="html", key="map_file")
    bar_chart_file = st.file_uploader("Upload your bar chart PNG file", type="png", key="bar_chart_file")
    text_summary_file = st.file_uploader("Upload your text summary CSV file", type="csv", key="text_summary_file")

    # Buttons
    submit_button = st.button("Submit")

    # Submit Files and Grade
    if submit_button:
        if student_id:
            grade = grade_assignment(code_input)
            update_google_sheet("", "", student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please enter a valid Student ID to submit your assignment.")
