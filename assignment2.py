import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys
import base64
from tempfile import NamedTemporaryFile
import os
import requests
import re

def show():
    # Apply the custom page style
    st.markdown(
        """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                color: #333;
            }
            .stButton > button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .stButton > button:hover {
                background-color: #45a049;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "bar_chart_png" not in st.session_state:
      st.session_state["bar_chart_png"] = None
    if "text_summary" not in st.session_state:
        st.session_state["text_summary"] = ""
    if "captured_output" not in st.session_state:
      st.session_state["captured_output"] = ""


    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Student ID Form
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:  # Verify student ID logic (placeholder)
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        Write a Python script that fetches real-time earthquake data from the USGS Earthquake API, filters earthquakes with a magnitude greater than 4.0, and visualizes the data on a map and as a bar chart.

        **Key Tasks:**
        1. Fetch earthquake data from the USGS API for the date range January 2nd, 2025, to January 9th, 2025.
        2. Filter earthquakes with a magnitude greater than 4.0.
        3. Visualize locations on a map with markers color-coded by magnitude range.
        4. Create a bar chart showing earthquake counts by magnitude ranges.
        5. Provide a text summary of the results.
        """)

    with tab2:
        st.markdown("""
        ### Grading Criteria
        - **Code Correctness (50%)**: The code should run without errors and produce the correct outputs.
        - **Visualization Quality (30%)**: The map and bar chart should be clear and informative.
        - **Code Quality (20%)**: The code should be well-structured, readable, and commented.
        """)


    # Section 3: Code Editor
    st.header("Step 3: Paste Your Colab Code Here")
    code = st.text_area("Paste your Python code here", height=300)

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["bar_chart_png"] = None
        st.session_state["text_summary"] = ""
        st.session_state["captured_output"] = ""


        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Execute the user's code
            local_context = {}

             # Define the scope for the user's code
            local_context['requests'] = requests
            local_context['pd'] = pd
            local_context['folium'] = folium
            local_context['plt'] = plt
            
            exec(code, local_context, local_context)

            # Capture execution output and errors
            st.session_state["captured_output"] = new_stdout.getvalue()

            # Mandatory Step Check: Fetch Data and Filter (simplified)
            if "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-01-02&endtime=2025-01-09" not in code:
                st.error("The code doesn't seem to use the correct USGS API URL with the date range.")
            elif "magnitude > 4.0" not in code:
               st.error("The code does not filter earthquakes with magnitude > 4.0.")
            else:
                 # Attempt to extract map, chart, and summary
                st.session_state["map_object"] = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)

                bar_chart = next((obj for obj in local_context.values() if isinstance(obj, plt.Figure)), None)
                if bar_chart:
                        # Save the matplotlib figure to a temporary file
                        with NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                            bar_chart.savefig(tmp_file.name)
                            temp_file_name = tmp_file.name

                        with open(temp_file_name, "rb") as img_file:
                           st.session_state["bar_chart_png"] = base64.b64encode(img_file.read()).decode("utf-8")
                        # Clean up the temporary file
                        os.remove(temp_file_name)

                # Attempt to extract a text summary from the captured output
                text_summary = st.session_state["captured_output"]

                # Modify the text summary to include the required information
                total_earthquakes_match = re.search(r"Total number of earthquakes with magnitude > 4\.0:\s*(\d+)", text_summary)
                avg_magnitude_match = re.search(r"Average magnitude:\s*([\d.]+)", text_summary)
                max_magnitude_match = re.search(r"Maximum magnitude:\s*([\d.]+)", text_summary)
                min_magnitude_match = re.search(r"Minimum magnitude:\s*([\d.]+)", text_summary)
                mag_range_4_5 = re.search(r"\*\s*4\.0-5\.0:\s*(\d+)", text_summary)
                mag_range_5_6 = re.search(r"\*\s*5\.0-6\.0:\s*(\d+)", text_summary)
                mag_range_6_plus = re.search(r"\*\s*6\.0\+:\s*(\d+)", text_summary)

                if total_earthquakes_match and avg_magnitude_match and max_magnitude_match and min_magnitude_match and mag_range_4_5 and mag_range_5_6 and mag_range_6_plus:
                       st.session_state["text_summary"] = f"""
                       Text Summary:
                       - Total number of earthquakes with magnitude > 4.0: {total_earthquakes_match.group(1)}
                       - Average magnitude: {float(avg_magnitude_match.group(1)):.2f}
                       - Maximum magnitude: {float(max_magnitude_match.group(1)):.2f}
                       - Minimum magnitude: {float(min_magnitude_match.group(1)):.2f}
                       - Number of earthquakes in each magnitude range:
                        * 4.0-5.0: {mag_range_4_5.group(1)}
                        * 5.0-6.0: {mag_range_5_6.group(1)}
                        * 6.0+: {mag_range_6_plus.group(1)}
                       """
                else:
                   st.session_state["text_summary"] = text_summary
                   st.warning("The text summary format might be incorrect. Please check your code and print the expected values with the expected format.")


                st.session_state["run_success"] = True
                st.success("Code executed successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state["captured_output"] = traceback.format_exc()
        finally:
            sys.stdout = old_stdout

        # Display captured output
        st.text_area("Code Output", st.session_state["captured_output"], height=200)

    # Section 4: Visualize Outputs
    st.header("Step 4: Visualize Your Outputs")
    if st.session_state.get("map_object"):
        st_folium(st.session_state["map_object"], width=700, height=500)

    if st.session_state.get("bar_chart_png"):
        st.markdown("### Bar Chart Output")
        st.image(f"data:image/png;base64,{st.session_state['bar_chart_png']}")

    if st.session_state.get("text_summary"):
         st.markdown("### Text Summary Output")
         st.text(st.session_state["text_summary"])


    # Section 5: Submit Assignment
    st.header("Step 5: Submit Your Assignment")
    submit_button = st.button("Submit Assignment")

    if submit_button:
        if st.session_state.get("run_success", False):
            st.success("Code submitted successfully! Your outputs have been recorded.")
            # Save submission logic here (e.g., Google Sheets or database)
        else:
            st.error("Please run your code successfully before submitting.")


if __name__ == "__main__":
    show()
