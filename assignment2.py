import streamlit as st
import traceback
import sys
from io import StringIO
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import folium
import pandas as pd

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Enter Student ID
    st.header("Section 1: Enter Your Student ID")
    with st.form("student_id_form"):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

    # Section 2: Review Assignment Details
    st.header("Section 2: Review Assignment Details")
    st.markdown("""
    ### Objective
    Write a Python script to:
    - Fetch earthquake data from the USGS API for January 2nd, 2025, to January 9th, 2025.
    - Filter earthquakes with a magnitude > 4.0.
    - Create:
        1. An interactive map showing earthquake locations.
        2. A bar chart of earthquake frequency by magnitude ranges.
        3. A text summary (total, average, max, and min magnitudes and earthquake counts by range).
    """)

    # Section 3: Run and Submit Your Code
    st.header("Section 3: Run and Submit Your Code")
    st.markdown("Paste your Python script below, then click **Run Code** to see your outputs.")

    code = st.text_area("Paste Your Python Code Here", height=300)

    # Initialize session state for outputs
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "captured_map" not in st.session_state:
        st.session_state["captured_map"] = None
    if "captured_bar_chart" not in st.session_state:
        st.session_state["captured_bar_chart"] = None
    if "captured_summary" not in st.session_state:
        st.session_state["captured_summary"] = None

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["captured_map"] = None
        st.session_state["captured_bar_chart"] = None
        st.session_state["captured_summary"] = None

        # Redirect stdout to capture print output
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            # Define a local execution environment
            exec_globals = {
                "st": st,
                "folium": folium,
                "pd": pd,
                "plt": plt,
            }

            # Execute the user-provided code
            exec(code, exec_globals)

            # Capture specific outputs if provided
            st.session_state["captured_map"] = exec_globals.get("mymap", None)
            st.session_state["captured_bar_chart"] = exec_globals.get("fig", None)
            st.session_state["captured_summary"] = exec_globals.get("summary_df", None)

            st.session_state["run_success"] = True
            st.success("Code executed successfully!")
        except Exception as e:
            st.error("An error occurred during code execution:")
            st.text(traceback.format_exc())
        finally:
            # Restore stdout
            sys.stdout = old_stdout

    # Display Outputs
    if st.session_state.get("run_success"):
        st.markdown("### Outputs")

        # Display the map if available
        if st.session_state["captured_map"]:
            st.markdown("#### Interactive Map")
            st_folium(st.session_state["captured_map"], width=700, height=500)
        else:
            st.warning("No map found. Ensure your script creates a map object named `mymap`.")

        # Display the bar chart if available
        if st.session_state["captured_bar_chart"]:
            st.markdown("#### Bar Chart")
            st.pyplot(st.session_state["captured_bar_chart"])
        else:
            st.warning("No bar chart found. Ensure your script creates a chart object named `fig`.")

        # Display the text summary if available
        if st.session_state["captured_summary"] is not None:
            st.markdown("#### Text Summary")
            st.dataframe(st.session_state["captured_summary"])
        else:
            st.warning("No summary found. Ensure your script creates a DataFrame object named `summary_df`.")

    # Section 4: Submit Assignment
    st.header("Section 4: Submit Your Assignment")
    if st.button("Submit Assignment"):
        if not st.session_state.get("run_success", False):
            st.error("Please run your code successfully before submitting.")
        else:
            st.success("Your code has been submitted successfully!")
            # Add submission logic here (e.g., save to Google Sheets or database)


if __name__ == "__main__":
    show()
