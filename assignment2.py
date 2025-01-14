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
    if 'map_created' not in st.session_state:
        st.session_state.map_created = None
    if 'chart_created' not in st.session_state:
        st.session_state.chart_created = None
    if 'summary_text' not in st.session_state:
        st.session_state.summary_text = None

    # Section 1: Student ID
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form"):
        student_id = st.text_input("Student ID (8 digits)")
        submit_id = st.form_submit_button("Verify ID")
        
        if submit_id:
            if validate_student_id(student_id):
                st.success("ID Verified")
                st.session_state.id_verified = True
            else:
                st.error("Please enter a valid 8-digit ID")
                st.session_state.id_verified = False

    # Section 2: Assignment Details
    st.header("Step 2: Review Assignment Details")
    with st.expander("View Assignment Requirements"):
        st.markdown("""
        ### Requirements:
        1. Fetch earthquake data from USGS API (Jan 2-9, 2025)
        2. Filter earthquakes with magnitude > 4.0
        3. Create visualizations:
           - Folium map with color-coded markers
           - Bar chart of earthquake frequencies by magnitude
        4. Generate summary statistics:
           - Total number of earthquakes
           - Average, maximum, and minimum magnitudes
           - Distribution across magnitude ranges
        """)

    # Section 3: Code Submission and Output
    st.header("Step 3: Run and Submit Your Code")
    
    code = st.text_area("Paste your Google Colab code here:", height=300)
    
    run_button = st.button("Run Code")
    
    if run_button and code.strip():
        # Capture stdout for summary statistics
        stdout_capture = StringIO()
        original_stdout = sys.stdout
        sys.stdout = stdout_capture
        
        try:
            # Modify the student's code to capture outputs
            modified_code = """
# Import necessary modules
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt

# Override display function to capture outputs
def display(obj):
    if isinstance(obj, folium.Map):
        st.session_state.map_created = obj
    elif isinstance(obj, pd.DataFrame):
        st.session_state.summary_text = obj
    
# Create a new figure for matplotlib
plt.figure(figsize=(10, 6))

# Execute the student's code
""" + code + """

# Capture the current figure if it exists
if plt.get_fignums():
    st.session_state.chart_created = plt.gcf()
"""
            
            # Create namespace for execution
            namespace = {
                'pd': pd,
                'plt': plt,
                'folium': folium,
                'st': st,
                'requests': requests,
                'MarkerCluster': MarkerCluster,
                'display': lambda x: None  # Placeholder that will be overridden
            }
            
            # Execute the modified code
            exec(modified_code, namespace)
            
            st.success("Code executed successfully!")
            
            # Display outputs
            if st.session_state.map_created is not None:
                st.subheader("Earthquake Map")
                st_folium(st.session_state.map_created, width=700, height=500)
            
            if st.session_state.chart_created is not None:
                st.subheader("Magnitude Distribution")
                st.pyplot(st.session_state.chart_created)
            
            if st.session_state.summary_text is not None:
                st.subheader("Summary Statistics")
                st.dataframe(st.session_state.summary_text)
            
            # Display any printed output
            output = stdout_capture.getvalue()
            if output.strip():
                st.subheader("Additional Output")
                st.text(output)
            
        except Exception as e:
            st.error(f"Error executing code: {str(e)}")
            st.code(traceback.format_exc())
        finally:
            sys.stdout = original_stdout
            plt.close('all')

    # Submit Button
    if st.button("Submit Assignment"):
        outputs_present = (
            st.session_state.map_created is not None and 
            st.session_state.chart_created is not None and 
            st.session_state.summary_text is not None
        )
        
        if not outputs_present:
            st.error("Please run your code successfully before submitting.")
        else:
            st.success("Assignment submitted successfully!")
            st.info(f"Submission recorded at: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    show()
