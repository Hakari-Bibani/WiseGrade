import streamlit as st
import folium
import pandas as pd
from io import StringIO
from streamlit_folium import st_folium
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import validate_student_id, update_google_sheet

def show():
    # Apply custom styles
    # Apply the custom page style
    set_page_style()

    # Initialize session state variables
@@ -51,63 +50,63 @@
        Fetch real-time earthquake data, process it, and visualize it through maps and charts.
        **Requirements:**
        1. Use the USGS Earthquake API to fetch data for the given date range.
        2. Filter earthquakes with magnitude > 4.0.
        3. Create an interactive map with earthquake locations and popups.
        4. Visualize earthquake frequency as a bar chart.
        5. Provide a text summary (e.g., number of earthquakes, average magnitude, etc.).
        - Use the USGS Earthquake API to fetch data.
        - Filter earthquakes with magnitude > 4.0.
        - Create an interactive map with earthquake locations and popups.
        - Visualize earthquake frequency as a bar chart.
        - Provide a text summary (e.g., number of earthquakes, average magnitude, etc.).
        """)

    with tab2:
        st.markdown("""
        ### Grading Breakdown
        1. **Code Implementation (30 points)**
        1. **Code Implementation (30 points)**:
           - Imports, API integration, and data filtering.
        2. **Visualization (40 points)**
        2. **Visualization (40 points)**:
           - Map, markers, popups, and bar chart.
        3. **Summary (30 points)**
        3. **Summary (30 points)**:
           - Accurate text-based statistics.
        """)

    # Section 3: Code Submission and Output
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

    # Run Code Button
    run_button = st.button("Run Code", key="run_code_button")
    if run_button and code_input:
        st.session_state["run_success"] = False
        st.session_state["captured_output"] = ""
        try:
            # Capture print statements
            captured_output = StringIO()
            import sys
            sys.stdout = captured_output

            # Execute user code
            local_context = {}
            exec(code_input, {}, local_context)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Capture results
            st.session_state["captured_output"] = captured_output.getvalue()
            st.session_state["map_object"] = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
            st.session_state["image_object"] = local_context.get("image_object", None)

            st.session_state["run_success"] = True
        except Exception as e:
            sys.stdout = sys.__stdout__
            st.error(f"An error occurred: {e}")

    # Display Outputs
    if st.session_state["run_success"]:
        st.markdown("### 📄 Captured Output")
        st.text(st.session_state["captured_output"])

        if st.session_state["map_object"]:
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["image_object"]:
