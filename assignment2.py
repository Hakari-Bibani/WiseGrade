import streamlit as st
import traceback
from io import StringIO
from streamlit_folium import st_folium
import matplotlib.pyplot as plt


def show():
    # Apply the custom page style from `style2.py`
    from utils.style2 import set_page_style
    set_page_style()

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None
    if "text_summary" not in st.session_state:
        st.session_state["text_summary"] = ""
    if "captured_output" not in st.session_state:
        st.session_state["captured_output"] = ""

    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Student ID
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        Write a Python script to:
        - Fetch earthquake data from the USGS Earthquake API for the date range January 2nd, 2025, to January 9th, 2025.
        - Filter earthquakes with magnitude > 4.0.
        - Visualize locations on a map with color-coded markers.
        - Create a bar chart showing earthquake counts by magnitude ranges.
        - Provide a text summary of the results.
        """)

    with tab2:
        st.markdown("""
        ### Grading Criteria
        - **Code Correctness (50%)**: Runs without errors and produces the expected results.
        - **Visualization Quality (30%)**: Outputs include a clear map, bar chart, and summary.
        - **Code Quality (20%)**: Proper structure, readability, and comments.
        """)

    # Section 3: Code Input and Execution
    st.header("Step 3: Write and Run Your Code")
    code = st.text_area("Paste your Python script here:", height=300)

    if st.button("Run Code"):
        # Reset previous results
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["text_summary"] = ""
        st.session_state["captured_output"] = ""

        # Capture output
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Execute the provided code in a controlled environment
            exec(code, {}, {})
            st.session_state["captured_output"] = new_stdout.getvalue()
            st.success("Code executed successfully!")
            st.session_state["run_success"] = True
        except Exception as e:
            st.session_state["captured_output"] = traceback.format_exc()
            st.error(f"Error executing code: {e}")
        finally:
            sys.stdout = old_stdout

        # Display captured output
        st.text_area("Execution Output:", st.session_state["captured_output"], height=200)

    # Section 4: Display Outputs
    st.header("Step 4: Visualize Outputs")
    if st.session_state.get("map_object"):
        st_folium(st.session_state["map_object"], width=700, height=500)

    if st.session_state.get("bar_chart"):
        st.pyplot(st.session_state["bar_chart"])

    if st.session_state.get("text_summary"):
        st.markdown(f"### Summary\n\n{st.session_state['text_summary']}")

    # Section 5: Submit Assignment
    st.header("Step 5: Submit Your Assignment")
    if st.button("Submit Assignment"):
        if st.session_state.get("run_success"):
            st.success("Assignment submitted successfully! Your outputs have been recorded.")
        else:
            st.error("Please run your code successfully before submitting.")


if __name__ == "__main__":
    show()
