import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from io import StringIO
import traceback
import sys

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
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None
    if "summary" not in st.session_state:
        st.session_state["summary"] = ""
    if "captured_output" not in st.session_state:
        st.session_state["captured_output"] = ""

    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Enter Student ID
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

    # Section 2: Assignment Details
    st.header("Step 2: Review Assignment Details")
    st.markdown("""
    ### Objective
    - Fetch earthquake data using the USGS Earthquake API.
    - Filter earthquakes with a magnitude greater than 4.0.
    - Visualize locations on a map with markers color-coded by magnitude range.
    - Create a bar chart showing earthquake counts by magnitude ranges.
    - Provide a text summary of the results.
    """)

    # Section 3: Run and Submit Code
    st.header("Step 3: Run and Submit Your Code")
    code_input = st.text_area("Paste your Python code here", height=300)

    run_button = st.button("Run Code")
    if run_button:
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["summary"] = ""
        st.session_state["captured_output"] = ""

        # Redirect stdout
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Execute the user's code
            local_context = {}
            exec(code_input, {}, local_context)

            # Capture outputs
            st.session_state["captured_output"] = new_stdout.getvalue()

            # Check for map object
            st.session_state["map_object"] = next(
                (obj for obj in local_context.values() if isinstance(obj, folium.Map)), None
            )

            # Check for bar chart
            st.session_state["bar_chart"] = next(
                (obj for obj in local_context.values() if isinstance(obj, plt.Figure)), None
            )

            # Check for text summary (e.g., DataFrame or print outputs)
            summary = ""
            for obj in local_context.values():
                if isinstance(obj, pd.DataFrame):
                    summary += obj.to_csv(index=False, float_format="%.2f")
            st.session_state["summary"] = summary

            st.session_state["run_success"] = True
            st.success("Code executed successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state["captured_output"] = traceback.format_exc()
        finally:
            sys.stdout = old_stdout

    # Display Outputs
    if st.session_state.get("run_success"):
        st.header("Outputs")
        if st.session_state.get("map_object"):
            st.markdown("### Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state.get("bar_chart"):
            st.markdown("### Bar Chart Output")
            st.pyplot(st.session_state["bar_chart"])

        if st.session_state.get("summary"):
            st.markdown("### Text Summary")
            st.text(st.session_state["summary"])

    # Submit Assignment
    st.header("Step 4: Submit Your Assignment")
    submit_button = st.button("Submit Assignment")

    if submit_button:
        if st.session_state.get("run_success"):
            st.success("Code submitted successfully!")
            # Logic to save submission (e.g., update Google Sheets)
        else:
            st.error("Please run your code successfully before submitting.")


if __name__ == "__main__":
    show()
