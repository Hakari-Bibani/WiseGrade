import streamlit as st
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet
import traceback
import folium
import pandas as pd

# Set the page style
set_page_style()

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Student Information Form
    with st.form("student_form", clear_on_submit=False):
        # Display Student ID (generated in Assignment 1)
        student_id = st.text_input("Student ID", key="student_id", help="Enter the Student ID generated in Assignment 1.")
        
        # Tabs for assignment and grading details
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("""
            ### Objective
            In this assignment, you will analyze real-time earthquake data from the USGS Earthquake API. You will filter earthquakes with a magnitude greater than 4.0, plot their locations on a map, and calculate statistics about the data.

            ### Assignment: Week 2 – Earthquake Data Analysis
            **Objective:**
            - Fetch earthquake data from the USGS Earthquake API for a specified date range.
            - Filter earthquakes with a magnitude greater than 4.0.
            - Plot the earthquake locations on an interactive map.
            - Calculate and display statistics about the earthquakes.
            """)
            # Add "See More" expandable section
            with st.expander("See More"):
                st.markdown("""
            **Task Requirements:**
            1. **Fetch Earthquake Data:**
               - Use the USGS Earthquake API to fetch data for the date range January 2nd, 2025, to January 9th, 2025.
               - The data should include latitude, longitude, magnitude, and time.

            2. **Filter Earthquakes:**
               - Filter the data to include only earthquakes with a magnitude greater than 4.0.

            3. **Map Visualization:**
               - Plot the filtered earthquake locations on an interactive map using `folium`.
               - Use color-coded markers based on magnitude:
                 - Green: 4.0-5.0
                 - Yellow: 5.0-5.5
                 - Red: 5.5+
               - Add popups to display additional information (magnitude, location, and time).

            4. **Statistics and Bar Chart:**
               - Calculate the number of earthquakes in the following magnitude ranges:
                 - 4.0-4.5
                 - 4.5-5.0
                 - 5.0+
               - Generate a bar chart to visualize the frequency of earthquakes in each range.
               - Provide a text summary with:
                 - Total number of earthquakes with magnitude > 4.0.
                 - Average, maximum, and minimum magnitudes.
                 - Number of earthquakes in each magnitude range.

            **Expected Output:**
            1. A map showing earthquake locations.
            2. A bar chart showing earthquake frequency by magnitude range.
            3. A text summary of earthquake statistics.
            """)

        with tab2:
            st.markdown("""
            ### Detailed Grading Breakdown
            (Grading details remain the same as shared earlier.)
            """)

        # Code Submission Area
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300, help="Paste your Python code here.")

        # Form Submit Buttons
        run_button = st.form_submit_button("Run")
        submit_button = st.form_submit_button("Submit")

    # Execute the code
    if run_button and code_input:
        try:
            # Create a local dictionary to capture code execution results
            local_context = {}
            exec(code_input, {}, local_context)

            # Search for outputs
            map_object = local_context.get('earthquake_map', None)
            dataframe_object = local_context.get('summary_df', None)

            # Display outputs
            if map_object:
                st.success("Map generated successfully!")
                map_object.save("earthquake_map.html")
                st.markdown("### 🗺️Generated Map")
                st.components.v1.html(map_object._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the code output.")

            if dataframe_object is not None:
                st.markdown("### 📊Earthquake Statistics")
                st.write(dataframe_object)
            else:
                st.warning("No DataFrame with earthquake statistics found in the code output.")

        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())

    # Submit and grade
    if submit_button and code_input:
        if student_id:
            grade = grade_assignment(code_input)
            update_google_sheet("N/A", "N/A", student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please enter your Student ID to submit your assignment.")
