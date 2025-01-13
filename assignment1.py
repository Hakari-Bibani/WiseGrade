import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import io
import sys

def capture_output(func):
    """
    Captures the output printed to the console.
    """
    captured_output = io.StringIO()  # Create a string buffer
    sys.stdout = captured_output  # Redirect stdout to the buffer
    try:
        func()
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout
    return captured_output.getvalue()

def find_folium_map(local_context):
    """
    Searches the local context for a Folium map object.
    """
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            return var_value
    return None

def find_dataframe(local_context):
    """
    Searches the local context for a Pandas DataFrame or similar.
    """
    for var_name, var_value in local_context.items():
        if isinstance(var_value, pd.DataFrame):
            return var_value
    return None

# Streamlit App UI
st.title("Dynamic Script Runner")

st.markdown(
    "Paste your Python script below. The app will automatically recognize your outputs and display them interactively."
)

# Code Input Area
code_input = st.text_area("Paste your Python code here", height=300)

# Buttons
run_button = st.button("Run Code")
if run_button and code_input:
    try:
        # Create a local dictionary for execution
        local_context = {}

        # Capture script output
        def run_script():
            exec(code_input, {}, local_context)

        script_output = capture_output(run_script)

        # Search for outputs
        map_object = find_folium_map(local_context)
        dataframe_object = find_dataframe(local_context)

        # Display the outputs
        if map_object:
            st.markdown("### 🗺️ Map Output")
            st_folium(map_object, width=700, height=500)
        else:
            st.warning("No Folium map was found in the script.")

        if dataframe_object is not None:
            st.markdown("### 📏 Distance Summary")
            st.dataframe(dataframe_object)
        else:
            st.warning("No DataFrame was found in the script.")

        # Display printed outputs
        if script_output.strip():
            st.markdown("### 📄 Printed Outputs")
            st.text(script_output)

    except Exception as e:
        st.error("An error occurred while running your code:")
        st.exception(e)
