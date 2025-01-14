import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from io import StringIO, BytesIO
import traceback
import sys


def execute_user_code(code):
    """
    Executes user-provided Python code and captures outputs.
    """
    local_context = {}
    stdout_buffer = StringIO()

    # Redirect stdout to capture print statements
    sys.stdout = stdout_buffer

    try:
        # Execute user code
        exec(code, {}, local_context)

        # Restore stdout
        sys.stdout = sys.__stdout__

        return local_context, stdout_buffer.getvalue(), None
    except Exception as e:
        # Restore stdout
        sys.stdout = sys.__stdout__
        return local_context, stdout_buffer.getvalue(), traceback.format_exc()


def find_folium_map(local_context):
    """
    Searches for a Folium map in the local execution context.
    """
    for obj in local_context.values():
        if isinstance(obj, folium.Map):
            return obj
    return None


def find_matplotlib_figure():
    """
    Captures the latest Matplotlib figure as a BytesIO object.
    """
    if plt.get_fignums():
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        return buffer
    return None


def find_dataframe(local_context):
    """
    Searches for a Pandas DataFrame in the local execution context.
    """
    for obj in local_context.values():
        if isinstance(obj, pd.DataFrame):
            return obj
    return None


def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    st.header("Step 1: Paste Your Script")
    code = st.text_area("Paste your Python script here", height=300)

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["detected_map"] = None
        st.session_state["detected_chart"] = None
        st.session_state["detected_summary"] = None

        # Execute user code and capture outputs
        local_context, stdout_output, error_output = execute_user_code(code)

        if error_output:
            st.error("An error occurred while executing your code:")
            st.text_area("Error Details", error_output, height=200)
        else:
            st.session_state["run_success"] = True

            # Detect outputs
            st.session_state["detected_map"] = find_folium_map(local_context)
            st.session_state["detected_chart"] = find_matplotlib_figure()
            st.session_state["detected_summary"] = find_dataframe(local_context)

            st.success("Code executed successfully!")
            st.text_area("Captured Output", stdout_output, height=200)

    # Section to display outputs
    st.header("Step 2: View Your Outputs")

    # Display Folium Map
    if st.session_state.get("detected_map"):
        st.subheader("Interactive Map")
        st_folium(st.session_state["detected_map"], width=700, height=500)
    else:
        st.warning("No map detected in the provided script.")

    # Display Bar Chart
    if st.session_state.get("detected_chart"):
        st.subheader("Bar Chart")
        st.image(st.session_state["detected_chart"], caption="Bar Chart Output", use_column_width=True)
    else:
        st.warning("No bar chart detected in the provided script.")

    # Display Text Summary
    if st.session_state.get("detected_summary") is not None:
        st.subheader("Text Summary (DataFrame)")
        st.dataframe(st.session_state["detected_summary"])
    else:
        st.warning("No text summary detected in the provided script.")

    # Allow submission if script executed successfully
    if st.session_state.get("run_success", False):
        if st.button("Submit Assignment"):
            st.success("Assignment submitted successfully! Your outputs have been recorded.")


if __name__ == "__main__":
    show()
