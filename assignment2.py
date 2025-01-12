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

            ### Task Requirements
            1. Fetch earthquake data from the USGS Earthquake API for January 2nd, 2025, to January 9th, 2025.
            2. Filter earthquakes with a magnitude greater than 4.0.
            3. Plot the earthquake locations on an interactive map using `folium`.
            4. Generate a bar chart for earthquake frequency by magnitude range.
            5. Provide a summary with statistics, including:
               - Total number of earthquakes.
               - Average, maximum, and minimum magnitudes.
               - Number of earthquakes in each magnitude range.

            **Expected Outputs:**
            - Interactive map showing earthquake locations.
            - Bar chart visualizing earthquake frequency.
            - A text summary of earthquake statistics.
            """)

        with tab2:
            st.markdown("""
            ### Grading Breakdown
            - **Code Structure (30 points):** Imports, API calls, error handling.
            - **Map Visualization (40 points):** Markers, color coding, and popups.
            - **Statistics and Bar Chart (30 points):** Filtering, chart accuracy, and summary.
            """)

        # Code Submission Area
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300, help="Paste your Python code here.")

        # Form Submit Buttons
        run_button = st.form_submit_button("Run")
        submit_button = st.form_submit_button("Submit")

    # Execute the code
    if run_button and code_input:
        try:
            # Sanitize input for invalid characters
            sanitized_code = code_input.replace('–', '-')

            # Create a local context to capture outputs
            local_context = {}
            exec(sanitized_code, {}, local_context)

            # Fetch outputs from the local context
            map_object = local_context.get('earthquake_map', None)
            dataframe_object = local_context.get('summary_df', None)

            # Display map output
            if map_object:
                st.success("Map generated successfully!")
                map_object.save("earthquake_map.html")
                st.markdown("### 🗺️ Earthquake Map")
                st.components.v1.html(map_object._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the output.")

            # Display DataFrame summary
            if dataframe_object is not None:
                st.markdown("### 📊 Earthquake Statistics")
                st.dataframe(dataframe_object)
            else:
                st.warning("No DataFrame with earthquake statistics found in the output.")

        except SyntaxError as se:
            st.error("Your code contains invalid characters or syntax:")
            st.error(se)
        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())

    # Submit and grade
    if submit_button and code_input:
        if student_id:
            try:
                grade = grade_assignment(code_input)
                update_google_sheet("N/A", "N/A", student_id, grade, "assignment_2")
                st.success(f"Submission successful! Your grade: {grade}/100")
            except Exception as e:
                st.error("An error occurred while grading your submission:")
                st.error(traceback.format_exc())
        else:
            st.error("Please enter your Student ID to submit your assignment.")
