import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import re
from io import StringIO
import traceback
from folium.plugins import MarkerCluster
import requests

def validate_student_id(student_id: str) -> bool:
    """Validates the student ID format (8 digits)"""
    return bool(re.match(r'^\d{8}$', student_id))

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Initialize session state for outputs
    if "outputs" not in st.session_state:
        st.session_state.outputs = {
            "map": None,
            "chart": None,
            "summary": None
        }

    # Step 1: Student ID
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Student ID (8 digits)")
    if student_id:
        if not validate_student_id(student_id):
            st.error("Please enter a valid 8-digit ID")

    # Step 2: Assignment Requirements
    st.header("Step 2: Review Assignment Details")
    with st.expander("View Requirements", expanded=False):
        st.markdown("""
        **Assignment Tasks**:
        1. Fetch earthquake data from the USGS API for January 2nd-9th, 2025.
        2. Filter earthquakes with a magnitude > 4.0.
        3. Create:
            - An interactive map with earthquake locations.
            - A bar chart showing earthquake counts by magnitude range.
            - A text summary with:
                - Total earthquakes with magnitude > 4.0.
                - Average, maximum, and minimum magnitudes.
                - Counts in magnitude ranges (e.g., 4-5, 5-6, 6+).
        """)

    # Step 3: Run User Code
    st.header("Step 3: Run and Submit Your Code")
    code = st.text_area("Paste your Google Colab code here:", height=300)

    if st.button("Run Code"):
        try:
            # Create namespace with custom display function for capturing outputs
            namespace = {
                'pd': pd,
                'plt': plt,
                'folium': folium,
                'requests': requests,
                'MarkerCluster': MarkerCluster,
                'st': st,
                'display': lambda obj: capture_output(obj)
            }

            def capture_output(obj):
                """Capture user-generated outputs"""
                if isinstance(obj, folium.Map):
                    st.session_state.outputs["map"] = obj
                elif isinstance(obj, plt.Figure):
                    st.session_state.outputs["chart"] = obj
                elif isinstance(obj, pd.DataFrame):
                    st.session_state.outputs["summary"] = obj

            # Pre-execution setup
            pre_code = """
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
"""

            # Post-execution capture
            post_code = """
# Capture current matplotlib figure
if plt.get_fignums():
    st.session_state.outputs["chart"] = plt.gcf()
"""

            # Execute user's code
            exec(pre_code + code + post_code, namespace)
            st.success("Code executed successfully!")

            # Display Map
            if st.session_state.outputs["map"]:
                st.subheader("Earthquake Map")
                st_folium(st.session_state.outputs["map"], width=700, height=500)
            else:
                st.warning("No map detected. Ensure your code generates a `folium.Map` object.")

            # Display Bar Chart
            if st.session_state.outputs["chart"]:
                st.subheader("Magnitude Distribution Bar Chart")
                st.pyplot(st.session_state.outputs["chart"])
            else:
                st.warning("No bar chart detected. Ensure your code generates a `matplotlib` or `seaborn` plot.")

            # Display Text Summary
            if st.session_state.outputs["summary"] is not None:
                st.subheader("Summary Statistics")
                st.dataframe(st.session_state.outputs["summary"])
            else:
                st.warning("No summary detected. Ensure your code generates a `pandas.DataFrame` for summary statistics.")

        except Exception as e:
            st.error("An error occurred while executing your code.")
            st.code(traceback.format_exc(), language="python")

    # Step 4: Submit Assignment
    if st.button("Submit Assignment"):
        if any(st.session_state.outputs.values()):
            st.success("Assignment submitted successfully!")
        else:
            st.error("Please run your code and generate outputs before submitting.")

if __name__ == "__main__":
    show()
