import streamlit as st
from streamlit_folium import st_folium
from io import StringIO
import traceback
import sys
import matplotlib.pyplot as plt
import pandas as pd
import folium


def show():
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
            # Use a safer exec environment to ignore unsupported imports
            exec_globals = {
                "st": st,
                "pd": pd,
                "plt": plt,
                "folium": folium,
                "__builtins__": __builtins__,
            }

            # Wrap the user's code in a try-except to catch import errors
            safe_code = f"""
try:
    {code}
except ImportError as e:
    print(f"Unsupported import ignored: {{e}}")
"""

            exec(safe_code, exec_globals)

            # Detect and capture outputs
            st.session_state["map_object"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, folium.Map)), None
            )
            st.session_state["bar_chart"] = plt.gcf() if plt.get_fignums() else None
            st.session_state["summary_text"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, pd.DataFrame)), None
            )

            st.session_state["run_success"] = True
            st.success("Code executed successfully!")
        except Exception as e:
            st.error(f"An error occurred while running your code: {e}")
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

        if st.session_state.get("summary_text") is not None:
            st.markdown("#### Text Summary")
            st.dataframe(st.session_state["summary_text"])

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
