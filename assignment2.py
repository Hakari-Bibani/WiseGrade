import streamlit as st
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet
import traceback

# Set the page style
set_page_style()

def show():
    st.title("Assignment 2: Real-Time Earthquake Data Analysis")

    # Student Information Form
    with st.form("student_form", clear_on_submit=False):
        # Field for Student ID
        student_id = st.text_input("Student ID", key="student_id")

        # Tabs for assignment and grading details
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("""
            ### Objective
            In this assignment, you will write a Python script that fetches real-time earthquake data from the USGS Earthquake API, processes the data to filter earthquakes with a magnitude greater than 4.0, and plots the earthquake locations on a map. Additionally, you will calculate the number of earthquakes in different magnitude ranges and present the results visually.

            ### Task Requirements
            - Use the USGS Earthquake API to fetch data for the date range **January 2nd, 2025, to January 9th, 2025**.
            - Filter the data to include only earthquakes with a magnitude greater than 4.0.
            - Create an interactive map that shows the locations of the filtered earthquakes.
            - Mark the earthquake locations on the map with markers, using different colors based on their magnitude:
                - **Green** for magnitude 4.0-4.5
                - **Yellow** for magnitude 4.5-5.0
                - **Red** for magnitude greater than 5.0
            - Add popups to display additional information about each earthquake (magnitude, location, and time).
            - Create a bar chart visualizing earthquake frequency by magnitude range:
                - 4.0-4.5
                - 4.5-5.0
                - Greater than 5.0
            - Generate a text summary as a CSV file containing:
                - Total number of earthquakes with magnitude > 4.0.
                - Average, maximum, and minimum magnitudes.
                - Number of earthquakes in each magnitude range.

            ### Python Libraries You Will Use
            - `folium` for the map.
            - `matplotlib` or `seaborn` for the bar chart.
            - `requests` or `urllib` for API calls.
            - `pandas` for data processing.

            ### Expected Output
            1. An interactive map showing earthquake locations.
            2. A bar chart visualizing earthquake frequency.
            3. A text summary (in CSV format).
            """)

        with tab2:
            st.markdown("""
            ### Detailed Grading Breakdown

            #### 1. Library Imports (10 Points)
            - **Points Allocation:**
                - `folium` for the map: 2 points
                - `matplotlib` or `seaborn` for the bar chart: 2 points
                - `requests` or `urllib` for API calls: 2 points
                - `pandas` for data processing: 2 points
                - Correct handling of library imports: 2 points

            #### 2. Data Processing and Filtering (40 Points)
            - Fetch earthquake data using the API: 10 points
            - Filter earthquakes with magnitude > 4.0: 10 points
            - Generate summary statistics: 10 points
            - Organize data into a structured format: 10 points

            #### 3. Map Visualization (30 Points)
            - Correctly plot earthquake locations: 10 points
            - Use appropriate marker colors for magnitude ranges: 10 points
            - Add informative popups: 10 points

            #### 4. Visualization and Summary (20 Points)
            - Generate bar chart for earthquake frequency: 10 points
            - Produce a detailed text summary: 10 points
            """)

        # Code Submission Area
        st.markdown("**📝 Paste Your Code Below:**")
        code_input = st.text_area("Paste your code here", height=200, key="code_input", placeholder="Paste your Python code here...")

        # Upload Fields for Generated Outputs
        st.markdown("### Upload Your Outputs")
        map_upload = st.file_uploader("Upload your map HTML file:", type=["html"], key="map_upload")
        chart_upload = st.file_uploader("Upload your bar chart PNG file:", type=["png"], key="chart_upload")
        summary_upload = st.file_uploader("Upload your text summary CSV file:", type=["csv"], key="summary_upload")

        # Submit Button
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if student_id:
            if code_input and map_upload and chart_upload and summary_upload:
                try:
                    # Grade the assignment
                    grade = grade_assignment(code_input)

                    # Update Google Sheet
                    update_google_sheet(None, None, student_id, grade, "assignment_2")

                    st.success(f"Submission successful! Your grade: {grade}/100")
                except Exception as e:
                    st.error("An error occurred during submission:")
                    st.error(traceback.format_exc())
            else:
                st.error("Please ensure you have provided your code, map file, chart file, and summary file.")
        else:
            st.error("Please enter your Student ID to proceed.")
