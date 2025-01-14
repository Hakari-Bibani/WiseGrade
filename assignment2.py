import streamlit as st
import traceback
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from io import StringIO
import sys
import re
from folium.plugins import MarkerCluster


def validate_student_id(student_id: str) -> bool:
    """Validates the student ID format (8 digits)."""
    return bool(re.match(r'^\d{8}$', student_id))


def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Initialize session state
    if "id_verified" not in st.session_state:
        st.session_state.id_verified = False
    if "map_object" not in st.session_state:
        st.session_state.map_object = None
    if "bar_chart" not in st.session_state:
        st.session_state.bar_chart = None
    if "summary_table" not in st.session_state:
        st.session_state.summary_table = None
    if "execution_logs" not in st.session_state:
        st.session_state.execution_logs = ""

    # Step 1: Student ID Verification
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form"):
        student_id = st.text_input("Student ID (8 digits)")
        submit_id = st.form_submit_button("Verify ID")

        if submit_id:
            if validate_student_id(student_id):
                st.success("Student ID Verified.")
                st.session_state.id_verified = True
            else:
                st.error("Invalid ID. Please enter an 8-digit Student ID.")
                st.session_state.id_verified = False

    # Step 2: Assignment Details
    st.header("Step 2: Review Assignment Details")
    with st.expander("View Assignment Requirements"):
        st.markdown("""
        ### Requirements:
        1. Fetch earthquake data from USGS API (Jan 2-9, 2025).
        2. Filter earthquakes with magnitude > 4.0.
        3. Create visualizations:
           - Folium map with color-coded markers.
           - Bar chart of earthquake frequencies by magnitude.
        4. Generate summary statistics:
           - Total number of earthquakes.
           - Average, maximum, and minimum magnitudes.
           - Distribution across magnitude ranges.
        """)

    # Step 3: Code Submission and Output
    st.header("Step 3: Run and Submit Your Code")
    code = st.text_area("Paste your Python code here:", height=300)
    run_button = st.button("Run Code")

    if run_button and code.strip():
        # Clear previous outputs
        st.session_state.map_object = None
        st.session_state.bar_chart = None
        st.session_state.summary_table = None
        st.session_state.execution_logs = ""

        # Capture stdout for printed output
        stdout_capture = StringIO()
        original_stdout = sys.stdout
        sys.stdout = stdout_capture

        try:
            # Execute the user's code
            namespace = {
                "pd": pd,
                "plt": plt,
                "folium": folium,
                "MarkerCluster": MarkerCluster,
            }
            exec(code, namespace)

            # Debugging: Display namespace content
            st.write("**Namespace Content After Execution**")
            st.write(namespace)

            # Detect outputs in the namespace
            st.session_state.map_object = next(
                (obj for obj in namespace.values() if isinstance(obj, folium.Map)), None
            )
            st.session_state.bar_chart = next(
                (obj for obj in namespace.values() if isinstance(obj, plt.Figure)), None
            )
            st.session_state.summary_table = next(
                (obj for obj in namespace.values() if isinstance(obj, pd.DataFrame)), None
            )

            st.success("Code executed successfully!")

        except Exception as e:
            st.error(f"Error executing code: {e}")
            st.session_state.execution_logs = traceback.format_exc()

        finally:
            sys.stdout = original_stdout

    # Step 4: Display Outputs
    st.header("Step 4: View Outputs")

    # Display Map
    if st.session_state.map_object:
        st.subheader("Earthquake Map")
        st_folium(st.session_state.map_object, width=700, height=500)
    else:
        st.warning("No map detected. Ensure your script outputs a Folium map object.")

    # Display Bar Chart
    if st.session_state.bar_chart:
        st.subheader("Magnitude Distribution")
        st.pyplot(st.session_state.bar_chart)
    else:
        st.warning("No bar chart detected. Ensure your script creates a Matplotlib figure.")

    # Display Summary Table
    if st.session_state.summary_table is not None:
        st.subheader("Summary Statistics")
        st.dataframe(st.session_state.summary_table)
    else:
        st.warning("No summary table detected. Ensure your script outputs a Pandas DataFrame.")

    # Show Execution Logs (if any)
    if st.session_state.execution_logs:
        st.subheader("Execution Logs")
        st.text(st.session_state.execution_logs)

    # Step 5: Submit Assignment
    st.header("Step 5: Submit Your Assignment")
    submit_button = st.button("Submit Assignment")

    if submit_button:
        if st.session_state.map_object and st.session_state.bar_chart and st.session_state.summary_table:
            st.success("Assignment submitted successfully!")
        else:
            st.error("Please ensure all outputs (map, bar chart, summary) are present before submitting.")


if __name__ == "__main__":
    show()
