import streamlit as st
import folium
import pandas as pd
from io import StringIO
from streamlit_folium import st_folium
from utils.style2 import set_page_style
from Record.google_sheet import check_student_id, update_google_sheet

def show():
    # Apply custom page style
    set_page_style()
@@ -47,101 +48,85 @@
        st.markdown("""
        ### Objective
        Write a Python script to fetch real-time earthquake data, filter it, and visualize it on a map and with a bar chart.
        
        **Steps:**
        - Fetch data using the USGS Earthquake API for the date range January 2nd, 2025, to January 9th, 2025.
        - Filter earthquakes with magnitude greater than 4.0.
        - Create a map with markers showing earthquake locations, colored by magnitude range.
        - Generate a bar chart showing earthquake frequencies in magnitude ranges.
        - Provide a summary of total earthquakes, statistics (min, max, average magnitude), and counts per range.
        """)
        with st.expander("See More"):
            st.markdown("""
        **API URL:**  
        `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-01-02&endtime=2025-01-09`
        **Python Libraries to Use:**  
        - `folium` for map visualization.
        - `matplotlib` or `seaborn` for bar chart plotting.
        - `requests` for API calls.
        - `pandas` for data processing.
        **Expected Output:**  
        1. Interactive map with earthquake markers.  
        2. Bar chart showing earthquake frequencies.  
        3. Summary with statistics and counts.
        """)

    with tab2:
        st.markdown("""
        ### Grading Criteria
        **1. Code Execution (30 points):**  
        - Full points if the script executes without errors.  
        **1. Code Execution (30 points):**
        - Full points if the script executes without errors.
        **2. Map Visualization (30 points):**  
        - Map generation (10 points).  
        - Correct markers and coloring (10 points).  
        - Popups for details (10 points).  
        **2. Map Visualization (30 points):**
        - Map generation (10 points).
        - Correct markers and coloring (10 points).
        - Popups for details (10 points).
        **3. Bar Chart and Summary (40 points):**  
        - Accurate bar chart (20 points).  
        - Correct statistical summary (20 points).  
        **3. Bar Chart and Summary (40 points):**
        - Accurate bar chart (20 points).
        - Correct statistical summary (20 points).
        """)

    # Section 3: Code Submission and Execution
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

    # Run Code Button
    run_button = st.button("Run Code", key="run_code_button")
    if run_button and code_input:
        st.session_state["run_success"] = False
        st.session_state["text_summary"] = ""
        try:
            # Redirect stdout to capture print statements
            captured_output = StringIO()
            import sys
            sys.stdout = captured_output

            # Execute the user's code
            local_context = {}
            exec(code_input, {}, local_context)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Capture outputs
            st.session_state["text_summary"] = captured_output.getvalue()
            st.session_state["map_object"] = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
            st.session_state["chart_image"] = next((obj for obj in local_context.values() if isinstance(obj, str) and obj.endswith(".png")), None)

            st.session_state["run_success"] = True
        except Exception as e:
            sys.stdout = sys.__stdout__
            st.error(f"An error occurred while running your code: {e}")

    # Display Outputs
    if st.session_state["run_success"]:
        st.markdown("### 📄 Captured Output")
        if st.session_state["text_summary"]:
            st.text(st.session_state["text_summary"])

        if st.session_state["map_object"]:
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["chart_image"]:
            st.markdown("### 📊 Bar Chart Output")
            st.image(st.session_state["chart_image"], caption="Bar Chart of Earthquake Frequencies")

    # Submit Code Button
    submit_button = st.button("Submit Code", key="submit_code_button")
    if submit_button:
        if not st.session_state.get("run_success", False):
            st.error("Please run your code successfully before submitting.")
        else:
            from grades.grade2 import grade_assignment

            grade = grade_assignment(code_input)
            update_google_sheet(st.session_state["verified_student_id"], grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
