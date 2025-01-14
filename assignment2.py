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
    Execute the user's code in a controlled sandboxed environment
    and capture map, bar chart, and text summary.
    """
    sandbox = {
        "folium": folium,
        "pd": pd,
        "plt": plt,
    }
    outputs = {
        "map": None,
        "bar_chart": None,
        "text_summary": None,
    }

    try:
        exec(code, sandbox)

        # Capture map object
        for obj in sandbox.values():
            if isinstance(obj, folium.Map):
                outputs["map"] = obj
                break

        # Capture bar chart
        if plt.get_fignums():
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            outputs["bar_chart"] = buffer
            plt.close()

        # Capture text summary (DataFrame)
        for obj in sandbox.values():
            if isinstance(obj, pd.DataFrame):
                outputs["text_summary"] = obj
                break

    except Exception as e:
        outputs["error"] = str(e)
        outputs["traceback"] = traceback.format_exc()

    return outputs


def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    st.header("Step 1: Paste Your Script")
    code = st.text_area("Paste your Python script here", height=300)

    if st.button("Run Code"):
        st.session_state["outputs"] = execute_user_code(code)

        if "error" in st.session_state["outputs"]:
            st.error(f"An error occurred: {st.session_state['outputs']['error']}")
            st.text_area("Error Details", st.session_state["outputs"]["traceback"], height=200)
        else:
            st.success("Code executed successfully!")

    # Section to display outputs
    st.header("Step 2: View Your Outputs")

    outputs = st.session_state.get("outputs", {})

    # Display Map
    if outputs.get("map"):
        st.subheader("Interactive Map")
        st_folium(outputs["map"], width=700, height=500)
    else:
        st.warning("No map detected in the provided script.")

    # Display Bar Chart
    if outputs.get("bar_chart"):
        st.subheader("Bar Chart")
        st.image(outputs["bar_chart"], caption="Earthquake Frequency by Magnitude", use_column_width=True)
    else:
        st.warning("No bar chart detected in the provided script.")

    # Display Text Summary
    if outputs.get("text_summary") is not None:
        st.subheader("Text Summary")
        st.dataframe(outputs["text_summary"])
    else:
        st.warning("No text summary detected in the provided script.")

    # Submission section
    st.header("Step 3: Submit Your Assignment")
    if st.button("Submit Assignment"):
        if "error" not in outputs:
            st.success("Assignment submitted successfully! Your outputs have been recorded.")
        else:
            st.error("Please fix the errors in your script before submitting.")


if __name__ == "__main__":
    show()
