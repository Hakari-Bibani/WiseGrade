import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import re
from io import StringIO
import sys
import traceback

def validate_student_id(student_id: str) -> bool:
    """Validates the student ID format (8 digits)"""
    return bool(re.match(r'^\d{8}$', student_id))

def extract_summary_stats(output_text: str) -> str:
    """Extract the summary statistics from print outputs"""
    # Look for common statistical patterns
    summary = []
    lines = output_text.split('\n')
    for line in lines:
        # Look for lines containing relevant statistical information
        if any(keyword in line.lower() for keyword in 
               ['total', 'average', 'maximum', 'minimum', 'earthquakes', 'magnitude']):
            summary.append(line.strip())
    return '\n'.join(summary)

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

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
    
    # Initialize session state for outputs
    if 'map_output' not in st.session_state:
        st.session_state.map_output = None
    if 'chart_output' not in st.session_state:
        st.session_state.chart_output = None
    if 'summary_output' not in st.session_state:
        st.session_state.summary_output = ""

    code = st.text_area("Paste your Google Colab code here:", height=300)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        run_button = st.button("Run Code")
    
    if run_button and code.strip():
        # Capture stdout for summary statistics
        stdout_capture = StringIO()
        sys.stdout = stdout_capture
        
        try:
            # Create figure before executing code to capture matplotlib output
            plt.figure()
            
            # Execute the code
            namespace = {
                'pd': pd,
                'plt': plt,
                'folium': folium,
                'st': st
            }
            exec(code, namespace)
            
            # Capture folium map
            for var in namespace.values():
                if isinstance(var, folium.Map):
                    st.session_state.map_output = var
            
            # Capture matplotlib figure
            fig = plt.gcf()
            if len(fig.axes) > 0:
                st.session_state.chart_output = fig
            
            # Capture printed output for summary
            sys.stdout = sys.__stdout__
            output_text = stdout_capture.getvalue()
            st.session_state.summary_output = extract_summary_stats(output_text)
            
            st.success("Code executed successfully!")
            
        except Exception as e:
            st.error(f"Error executing code: {str(e)}")
            st.code(traceback.format_exc())
        finally:
            sys.stdout = sys.__stdout__
            plt.close('all')

    # Display Outputs
    if st.session_state.map_output:
        st.subheader("Earthquake Map")
        st_folium(st.session_state.map_output, width=700, height=500)

    if st.session_state.chart_output:
        st.subheader("Magnitude Distribution")
        st.pyplot(st.session_state.chart_output)

    if st.session_state.summary_output:
        st.subheader("Summary Statistics")
        st.text(st.session_state.summary_output)

    # Submit Button
    if st.button("Submit Assignment"):
        if not (st.session_state.map_output and 
                st.session_state.chart_output and 
                st.session_state.summary_output):
            st.error("Please run your code successfully before submitting.")
        else:
            st.success("Assignment submitted successfully!")
            # Add submission timestamp
            st.info(f"Submission recorded at: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    show()
