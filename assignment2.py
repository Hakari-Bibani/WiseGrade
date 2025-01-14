import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import re
from io import StringIO
import sys
import traceback
from folium.plugins import MarkerCluster
import requests

def validate_student_id(student_id: str) -> bool:
    """Validates the student ID format (8 digits)"""
    return bool(re.match(r'^\d{8}$', student_id))

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Initialize session state
    if "outputs" not in st.session_state:
        st.session_state.outputs = {
            "map": None,
            "chart": None,
            "summary": None
        }

    # Section 1: Student ID
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Student ID (8 digits)")
    if student_id:
        if not validate_student_id(student_id):
            st.error("Please enter a valid 8-digit ID")

    # Section 2: Review Requirements
    st.header("Step 2: Review Assignment Details")
    with st.expander("View Requirements", expanded=False):
        st.markdown("""
        1. Fetch earthquake data from USGS API (Jan 2-9, 2025)
        2. Filter earthquakes with magnitude > 4.0
        3. Create visualizations and summary
        """)

    # Section 3: Code Input and Execution
    st.header("Step 3: Run and Submit Your Code")
    code = st.text_area("Paste your Google Colab code here:", height=300)
    
    if st.button("Run Code"):
        try:
            # Create namespace with modified display function
            namespace = {
                'pd': pd,
                'plt': plt,
                'folium': folium,
                'requests': requests,
                'MarkerCluster': MarkerCluster,
                'st': st,
                'display': lambda x: None
            }

            # Add capture code
            capture_code = """
# Function to capture outputs
def display(obj):
    if isinstance(obj, folium.Map):
        st.session_state.outputs["map"] = obj
    elif isinstance(obj, pd.DataFrame):
        st.session_state.outputs["summary"] = obj
"""

            # Add figure capture
            pre_code = """
plt.figure(figsize=(10, 6))
"""

            # Add post-execution capture
            post_code = """
# Capture the current figure
if plt.get_fignums():
    st.session_state.outputs["chart"] = plt.gcf()
"""

            # Execute all code
            exec(capture_code + pre_code + code + post_code, namespace)
            st.success("Code executed successfully!")

            # Display Map
            if st.session_state.outputs["map"]:
                st.subheader("Earthquake Map")
                st_folium(st.session_state.outputs["map"], width=700, height=500)

            # Display Chart
            if st.session_state.outputs["chart"]:
                st.subheader("Magnitude Distribution")
                st.pyplot(st.session_state.outputs["chart"])

            # Display Summary
            if st.session_state.outputs["summary"] is not None:
                st.subheader("Summary Statistics")
                st.dataframe(st.session_state.outputs["summary"])

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.code(traceback.format_exc())

    # Submit button
    if st.button("Submit Assignment"):
        outputs_present = all(st.session_state.outputs.values())
        if outputs_present:
            st.success("Assignment submitted successfully!")
        else:
            st.error("Please run your code successfully before submitting.")

if __name__ == "__main__":
    show()
