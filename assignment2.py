import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from streamlit_folium import st_folium
import traceback
import sys

def show():
    st.markdown(
        """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                color: #333;
            }
            .stButton > button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .stButton > button:hover {
                background-color: #45a049;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_html" not in st.session_state:
        st.session_state["map_html"] = None
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None
    if "text_summary" not in st.session_state:
        st.session_state["text_summary"] = None
    if "captured_output" not in st.session_state:
        st.session_state["captured_output"] = ""

    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Student ID Form
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

    # Section 2: Assignment Details
    st.header("Step 2: Assignment Details")
    st.markdown("""
    ### Objective
    - Fetch real-time earthquake data using the USGS Earthquake API.
    - Filter and visualize the data:
      - Interactive map with earthquake locations.
      - Bar chart of earthquake counts by magnitude range.
    - Provide a text summary of the results.
    """)

    # Section 3: Code Submission
    st.header("Step 3: Submit and Run Your Code")
    code = st.text_area("Paste your Python code here", height=300)

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["map_html"] = None
        st.session_state["bar_chart"] = None
        st.session_state["text_summary"] = None
        st.session_state["captured_output"] = ""

        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Execute the user's code
            local_context = {}
            exec(code, {}, local_context)

            st.session_state["captured_output"] = new_stdout.getvalue()

            # Extract main outputs
            # 1. Detect saved HTML map
            if "earthquake_map.html" in local_context.get("earthquake_map", ""):
                with open("earthquake_map.html", "r") as file:
                    st.session_state["map_html"] = file.read()

            # 2. Detect bar chart saved as PNG
            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.session_state["bar_chart"] = buf

            # 3. Detect text summary (CSV output)
            if "earthquake_summary.csv" in local_context.get("summary_df", ""):
                st.session_state["text_summary"] = local_context["summary_df"]

            st.session_state["run_success"] = True
            st.success("Code executed successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state["captured_output"] = traceback.format_exc()
        finally:
            sys.stdout = old_stdout

        st.text_area("Code Output", st.session_state["captured_output"], height=200)

    # Section 4: Display Outputs
    st.header("Step 4: Visualize Your Outputs")

    if st.session_state.get("map_html"):
        st.markdown("### Interactive Map")
        st.components.v1.html(st.session_state["map_html"], height=500)

    if st.session_state.get("bar_chart"):
        st.markdown("### Bar Chart")
        st.image(st.session_state["bar_chart"])

    if st.session_state.get("text_summary") is not None:
        st.markdown("### Text Summary (CSV)")
        st.download_button(
            label="Download Summary CSV",
            data=st.session_state["text_summary"].to_csv(index=False),
            file_name="earthquake_summary.csv",
            mime="text/csv"
        )

    # Section 5: Submit Assignment
    st.header("Step 5: Submit Your Assignment")
    submit_button = st.button("Submit Assignment")

    if submit_button:
        if st.session_state.get("run_success", False):
            st.success("Code submitted successfully! Your outputs have been recorded.")
            # Save submission logic here (e.g., Google Sheets or database)
        else:
            st.error("Please run your code successfully before submitting.")


if __name__ == "__main__":
    show()
