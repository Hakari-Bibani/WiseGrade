import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from streamlit_folium import st_folium
import traceback
import sys


def detect_outputs(local_context):
    """
    Detect and capture the main outputs (map, PNG bar chart, text summary) 
    from the user's script.
    """
    detected_outputs = {
        "map": None,
        "bar_chart": None,
        "text_summary": None,
    }

    # Detect Folium Map
    detected_outputs["map"] = next(
        (obj for obj in local_context.values() if isinstance(obj, folium.Map)), None
    )

    # Detect Pandas DataFrame (assumed for text summary)
    detected_outputs["text_summary"] = next(
        (obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None
    )

    # Detect Matplotlib Figure (bar chart)
    detected_outputs["bar_chart"] = plt.gcf() if plt.get_fignums() else None

    return detected_outputs


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
        unsafe_allow_html=True,
    )

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "captured_output" not in st.session_state:
        st.session_state["captured_output"] = ""
    if "detected_outputs" not in st.session_state:
        st.session_state["detected_outputs"] = {}

    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Student ID Form
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:  # Placeholder for verifying student ID
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

    # Section 2: Code Editor
    st.header("Step 2: Paste Your Script")
    code = st.text_area("Paste your Python script here", height=300)

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["captured_output"] = ""
        st.session_state["detected_outputs"] = {}

        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Execute the user's code
            local_context = {}
            exec(code, {}, local_context)
            st.session_state["run_success"] = True
            st.session_state["captured_output"] = new_stdout.getvalue()

            # Detect main outputs
            st.session_state["detected_outputs"] = detect_outputs(local_context)
            st.success("Code executed successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state["captured_output"] = traceback.format_exc()
        finally:
            sys.stdout = old_stdout

        # Display captured output
        st.text_area("Code Output", st.session_state["captured_output"], height=200)

    # Section 3: Display Outputs
    st.header("Step 3: View Your Outputs")

    detected_outputs = st.session_state.get("detected_outputs", {})

    # Display Folium Map
    if detected_outputs.get("map"):
        st.subheader("Interactive Map")
        st_folium(detected_outputs["map"], width=700, height=500)
    else:
        st.warning("No map detected in the provided script.")

    # Display Bar Chart
    if detected_outputs.get("bar_chart"):
        st.subheader("Bar Chart (PNG)")
        buffer = BytesIO()
        detected_outputs["bar_chart"].savefig(buffer, format="png")
        st.image(buffer, caption="Earthquake Frequency by Magnitude", use_column_width=True)
    else:
        st.warning("No bar chart detected in the provided script.")

    # Display Text Summary
    if detected_outputs.get("text_summary") is not None:
        st.subheader("Text Summary (DataFrame)")
        st.dataframe(detected_outputs["text_summary"])
    else:
        st.warning("No text summary detected in the provided script.")

    # Section 4: Submit Assignment
    st.header("Step 4: Submit Your Assignment")
    if st.button("Submit Assignment"):
        if st.session_state.get("run_success", False):
            st.success("Assignment submitted successfully! Your outputs have been recorded.")
            # Save submission logic here (e.g., Google Sheets or database)
        else:
            st.error("Please run your code successfully before submitting.")


if __name__ == "__main__":
    show()
