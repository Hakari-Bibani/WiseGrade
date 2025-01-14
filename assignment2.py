import streamlit as st
import traceback
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from io import StringIO
import sys

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
            # Modify code to ignore Colab-specific modules
            safe_code = code.replace("import google.colab", "# Colab import removed")
            safe_code = safe_code.replace("google.colab.files.download", "# Colab download removed")

            # Execute the user's code in a controlled environment
            exec_globals = {
                "st": st,
                "pd": pd,
                "plt": plt,
                "folium": folium,
            }
            exec(safe_code, exec_globals)

            # Detect and capture outputs
            st.session_state["map_object"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, folium.Map)), None
            )
            st.session_state["bar_chart"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, plt.Figure)), None
            )
            st.session_state["summary_text"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, pd.DataFrame)), None
            )

            st.session_state["run_success"] = True
            st.success("Code executed successfully!")
        except Exception as e:
            st.error("An error occurred while executing your code.")
            st.text_area("Error Details", traceback.format_exc(), height=200)
        finally:
            sys.stdout = old_stdout

    # Display Outputs
    if st.session_state.get("run_success"):
        st.markdown("### Outputs")

        # Display Map
        if st.session_state.get("map_object"):
            st.markdown("#### Interactive Map")
            st_folium(st.session_state["map_object"], width=700, height=500)
        else:
            st.warning("No map object detected in your code.")

        # Display Bar Chart
        if st.session_state.get("bar_chart"):
            st.markdown("#### Bar Chart")
            st.pyplot(st.session_state["bar_chart"])
        else:
            st.warning("No bar chart detected in your code.")

        # Display Text Summary
        if st.session_state.get("summary_text") is not None:
            st.markdown("#### Text Summary")
            st.dataframe(st.session_state["summary_text"])
        else:
            st.warning("No text summary detected in your code.")

    # Section 4: Submit Assignment
    st.header("Section 4: Submit Your Assignment")
    if st.button("Submit Assignment"):
        if not st.session_state.get("run_success", False):
            st.error("Please run your code successfully before submitting.")
        else:
            st.success("Your code has been submitted successfully!")
            # Add logic to save the submission (e.g., Google Sheets or database)


if __name__ == "__main__":
    show()
