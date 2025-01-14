import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys


def show():
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
        unsafe_allow_html=True,
    )

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None
    if "summary_text" not in st.session_state:
        st.session_state["summary_text"] = None

    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Enter Your Student ID
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

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["summary_text"] = None

        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Execute the user's code
            exec_globals = {
                "st": st,
                "folium": folium,
                "pd": pd,
                "plt": plt,
            }
            exec(code, exec_globals)

            # Retrieve outputs if they exist
            st.session_state["map_object"] = exec_globals.get("map_object", None)
            st.session_state["bar_chart"] = exec_globals.get("bar_chart", None)
            st.session_state["summary_text"] = exec_globals.get("summary_text", None)

            st.session_state["run_success"] = True
            st.success("Code executed successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.text_area("Error Details", traceback.format_exc(), height=200)
        finally:
            sys.stdout = old_stdout

    # Display outputs
    st.markdown("### Outputs")
    if st.session_state.get("run_success"):
        if st.session_state.get("map_object"):
            st.markdown("#### Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state.get("bar_chart"):
            st.markdown("#### Bar Chart Output")
            st.pyplot(st.session_state["bar_chart"])

        if st.session_state.get("summary_text"):
            st.markdown("#### Text Summary")
            st.text(st.session_state["summary_text"])

    # Submit Code Button
    st.header("Submit Your Code")
    if st.button("Submit Assignment"):
        if not st.session_state.get("run_success", False):
            st.error("Please run your code successfully before submitting.")
        else:
            st.success("Your code has been submitted successfully!")
            # Add code to save submission (e.g., Google Sheets or a database)


if __name__ == "__main__":
    show()
