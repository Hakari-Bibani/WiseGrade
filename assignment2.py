import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from io import StringIO
import traceback
import sys
import os
from matplotlib import pyplot as plt
from PIL import Image

def run_user_script(code_input):
    """
    Executes the user-provided script and extracts key outputs.
    """
    # Initialize storage for outputs
    outputs = {"map": None, "bar_chart_path": None, "text_summary": None, "errors": None}

    # Redirect stdout to capture print output
    old_stdout = sys.stdout
    captured_output = StringIO()
    sys.stdout = captured_output

    try:
        # Execute the user's code in a controlled environment
        local_context = {}
        exec(code_input, {}, local_context)

        # Detect `folium` map
        map_object = next((v for v in local_context.values() if isinstance(v, folium.Map)), None)
        if map_object:
            map_file = "temp_map.html"
            map_object.save(map_file)
            outputs["map"] = map_file

        # Detect bar chart saved as an image
        bar_chart_path = next(
            (v for v in local_context.values() if isinstance(v, str) and v.endswith(".png")), None
        )
        if bar_chart_path and os.path.exists(bar_chart_path):
            outputs["bar_chart_path"] = bar_chart_path

        # Detect text summary (assumed to be a pandas DataFrame)
        text_summary = next((v for v in local_context.values() if isinstance(v, pd.DataFrame)), None)
        if text_summary is not None:
            outputs["text_summary"] = text_summary

    except Exception as e:
        outputs["errors"] = traceback.format_exc()

    # Restore stdout
    sys.stdout = old_stdout

    return outputs, captured_output.getvalue()

def show():
    """
    Main function to render the Streamlit app.
    """
    st.title("Assignment 2: Earthquake Data Analysis Viewer")

    st.markdown("""
    Paste your Python script below. This app will execute the code and display:
    - An interactive `folium` map.
    - A bar chart image created with `matplotlib` or `seaborn`.
    - A text summary created using `pandas`.
    """)

    # Text Area for Code Input
    st.header("Step 1: Enter Your Code")
    code_input = st.text_area("Paste your Python script here:", height=300)

    if st.button("Run Code"):
        with st.spinner("Running your code..."):
            # Run user script and extract outputs
            outputs, captured_output = run_user_script(code_input)

        # Handle errors
        if outputs["errors"]:
            st.error("An error occurred while running your code:")
            st.text(outputs["errors"])
        else:
            st.success("Code executed successfully!")

            # Display Map
            if outputs["map"]:
                st.subheader("Interactive Map")
                st_folium(outputs["map"], width=700, height=500)
            else:
                st.warning("No `folium` map detected in your script.")

            # Display Bar Chart
            if outputs["bar_chart_path"]:
                st.subheader("Bar Chart")
                try:
                    img = Image.open(outputs["bar_chart_path"])
                    st.image(img, use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying the bar chart: {e}")
            else:
                st.warning("No bar chart image detected in your script.")

            # Display Text Summary
            if outputs["text_summary"] is not None:
                st.subheader("Text Summary")
                st.dataframe(outputs["text_summary"])
            else:
                st.warning("No text summary detected in your script.")

        # Display Captured Output
        if captured_output:
            st.subheader("Captured Output")
            st.text(captured_output)

if __name__ == "__main__":
    show()
