import streamlit as st
import traceback
from io import StringIO
from streamlit_folium import st_folium
import sys

# Section 1: Enter Your Student ID
def student_id_section():
    st.header("Section 1: Enter Your Student ID")
    with st.form("student_id_form"):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:
                st.success(f"Student ID {student_id} verified. You may proceed.")
                return True
            else:
                st.error("Please provide a valid Student ID.")
    return False

# Section 2: Review Assignment Details
def assignment_details_section():
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

# Section 3: Run and Submit User Code
def run_user_code_section():
    st.header("Section 3: Run and Submit Your Code")
    st.markdown("Paste your Python script below, then click **Run Code** to see your outputs.")

    code = st.text_area("Paste Your Python Code Here", height=300)

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["text_summary"] = None

        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Execute the user's code in a dynamic environment
            exec_globals = {}
            exec(code, exec_globals)

            # Detect and store map output
            map_object = next((value for value in exec_globals.values() if "folium.folium.Map" in str(type(value))), None)
            if map_object:
                st.session_state["map_object"] = map_object

            # Detect and store bar chart output
            bar_chart = next((value for value in exec_globals.values() if "matplotlib.figure.Figure" in str(type(value))), None)
            if bar_chart:
                st.session_state["bar_chart"] = bar_chart

            # Detect and store text summary
            summary_df = next((value for value in exec_globals.values() if "pandas.core.frame.DataFrame" in str(type(value))), None)
            if summary_df is not None:
                st.session_state["text_summary"] = summary_df

            st.session_state["run_success"] = True
            st.success("Code executed successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.text_area("Error Details", traceback.format_exc(), height=200)
        finally:
            sys.stdout = old_stdout

    # Display outputs if the code ran successfully
    if st.session_state.get("run_success"):
        st.markdown("### Outputs")
        if st.session_state.get("map_object"):
            st.markdown("#### Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state.get("bar_chart"):
            st.markdown("#### Bar Chart Output")
            st.pyplot(st.session_state["bar_chart"])

        if st.session_state.get("text_summary") is not None:
            st.markdown("#### Text Summary")
            st.dataframe(st.session_state["text_summary"])

# Section 4: Submission
def submit_code_section():
    st.header("Section 4: Submit Your Assignment")
    if st.button("Submit Assignment"):
        if st.session_state.get("run_success", False):
            st.success("Your code has been submitted successfully!")
            # Save submission logic here (e.g., Google Sheets or a database)
        else:
            st.error("Please run your code successfully before submitting.")

# Main Application Flow
def show():
    if student_id_section():
        assignment_details_section()
        run_user_code_section()
        submit_code_section()

if __name__ == "__main__":
    show()
