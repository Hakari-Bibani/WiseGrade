import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from io import StringIO, BytesIO
import traceback
import sys
import os

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

    # Detect Matplotlib Figure (bar chart)
    detected_outputs["bar_chart"] = plt.gcf() if plt.get_fignums() else None

    # Detect Pandas DataFrame (text summary)
    detected_outputs["text_summary"] = next(
        (obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None
    )

    return detected_outputs


def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    st.header("Step 1: Paste Your Script")
    code = st.text_area("Paste your Python script here", height=300)

    if st.button("Run Code"):
        st.session_state["run_success"] = False
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

            # Detect outputs
            st.session_state["detected_outputs"] = detect_outputs(local_context)
            st.success("Code executed successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.text_area("Error Details", traceback.format_exc(), height=200)
        finally:
            sys.stdout = old_stdout

    # Section to display outputs
    st.header("Step 2: View Your Outputs")
    detected_outputs = st.session_state.get("detected_outputs", {})

    # Display Folium Map
    if detected_outputs.get("map"):
        st.subheader("Interactive Map")
        st_folium(detected_outputs["map"], width=700, height=500)
    else:
        st.warning("No map detected in the provided script.")

    # Display Bar Chart
    if detected_outputs.get("bar_chart"):
        st.subheader("Bar Chart")
        buffer = BytesIO()
        detected_outputs["bar_chart"].savefig(buffer, format="png")
        buffer.seek(0)
        st.image(buffer, caption="Earthquake Frequency by Magnitude", use_column_width=True)
    else:
        st.warning("No bar chart detected in the provided script.")

    # Display Text Summary
    if detected_outputs.get("text_summary") is not None:
        st.subheader("Text Summary (DataFrame)")
        st.dataframe(detected_outputs["text_summary"])
    else:
        st.warning("No text summary detected in the provided script.")

    # Allow submission if script executed successfully
    if st.session_state.get("run_success", False):
        if st.button("Submit Assignment"):
            st.success("Assignment submitted successfully! Your outputs have been recorded.")


if __name__ == "__main__":
    show()
