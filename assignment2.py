import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys

def show():
    st.title("Assignment 2: Earthquake Data Analysis Viewer")

    st.markdown("""
    This app dynamically processes your Python script entered below and displays its outputs:
    - An interactive `folium` map.
    - A bar chart generated with `matplotlib` or `seaborn`.
    - A text summary created using `pandas`.
    """)

    # Text Area for Code Input
    st.header("Step 1: Enter Your Code")
    code_input = st.text_area("Paste your Python script here:", height=300)

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["text_summary"] = None
        st.session_state["captured_output"] = ""

        # Redirect stdout to capture print output
        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Execute the user's code
            local_context = {}
            exec(code_input, {}, local_context)

            # Restore stdout
            sys.stdout = old_stdout
            st.session_state["run_success"] = True
            st.session_state["captured_output"] = captured_output.getvalue()

            # Detect key outputs
            map_object = next((v for v in local_context.values() if isinstance(v, folium.Map)), None)
            bar_chart_path = next((v for v in local_context.values() if isinstance(v, str) and v.endswith(".png")), None)
            text_summary = next((v for v in local_context.values() if isinstance(v, pd.DataFrame)), None)

            st.session_state["map_object"] = map_object
            st.session_state["bar_chart"] = bar_chart_path
            st.session_state["text_summary"] = text_summary

        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"An error occurred while running your script:\n{traceback.format_exc()}")

        # Display Outputs
        if st.session_state.get("run_success"):
            st.header("Step 2: Results")

            # Display Map
            if st.session_state.get("map_object"):
                st.subheader("Interactive Map")
                st_folium(st.session_state["map_object"], width=700, height=500)
            else:
                st.warning("No `folium` map object detected in your script.")

            # Display Bar Chart
            if st.session_state.get("bar_chart"):
                st.subheader("Bar Chart")
                try:
                    image_path = st.session_state["bar_chart"]
                    st.image(image_path, use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying the bar chart: {e}")
            else:
                st.warning("No bar chart file detected in your script.")

            # Display Text Summary
            if st.session_state.get("text_summary") is not None:
                st.subheader("Text Summary")
                st.dataframe(st.session_state["text_summary"])
            else:
                st.warning("No text summary detected in your script.")

        # Display Captured Output
        if st.session_state.get("captured_output"):
            st.subheader("Captured Output")
            st.text(st.session_state["captured_output"])

if __name__ == "__main__":
    show()
