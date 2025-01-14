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
            exec(code, {}, local_context)
            st.session_state["run_success"] = True
            st.session_state["captured_output"] = new_stdout.getvalue()


            # Extract the folium map object
            map_object = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
            st.session_state["map_object"] = map_object
            
            # Extract the matplotlib figure and save as a png
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
            st.session_state["text_summary"] = st.session_state["captured_output"]

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
