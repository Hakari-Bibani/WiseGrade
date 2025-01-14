import streamlit as st
import traceback
import folium
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from io import StringIO
import sys
import os

def show():
    st.title("Assignment 2: Earthquake Data Analysis Viewer")
    st.markdown("""
    Upload your Python script here, and this application will automatically run it to display the key outputs:
    1. An interactive HTML map using `folium`.
    2. A PNG bar chart created with `matplotlib` or `seaborn`.
    3. A text summary using `pandas`.
    """)

    # File Upload
    uploaded_file = st.file_uploader("Upload your Python script", type=["py"])

    if uploaded_file:
        # Save the uploaded script
        script_path = os.path.join("uploaded_script.py")
        with open(script_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("Script uploaded successfully!")
        run_button = st.button("Run Script")

        if run_button:
            st.session_state["run_success"] = False
            st.session_state["captured_output"] = ""
            st.session_state["map_object"] = None
            st.session_state["bar_chart"] = None
            st.session_state["text_summary"] = None

            # Redirect stdout to capture print output
            old_stdout = sys.stdout
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                # Execute the script
                local_context = {}
                exec(open(script_path).read(), {}, local_context)

                # Restore stdout
                sys.stdout = old_stdout
                st.session_state["run_success"] = True
                st.session_state["captured_output"] = captured_output.getvalue()

                # Extract outputs
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
                st.markdown("### Outputs")
                
                # Map
                if st.session_state.get("map_object"):
                    st.markdown("#### Interactive Map")
                    st_folium(st.session_state["map_object"], width=700, height=500)
                else:
                    st.warning("No map object found in your script.")

                # Bar Chart
                if st.session_state.get("bar_chart"):
                    st.markdown("#### Bar Chart")
                    try:
                        image_path = st.session_state["bar_chart"]
                        if os.path.exists(image_path):
                            st.image(image_path, use_column_width=True)
                        else:
                            st.warning(f"Bar chart file '{image_path}' not found.")
                    except Exception as e:
                        st.error(f"Error displaying the bar chart: {e}")
                else:
                    st.warning("No bar chart file found in your script.")

                # Text Summary
                if st.session_state.get("text_summary") is not None:
                    st.markdown("#### Text Summary")
                    st.dataframe(st.session_state["text_summary"])
                else:
                    st.warning("No text summary found in your script.")

            # Display Captured Output
            if st.session_state.get("captured_output"):
                st.markdown("### Captured Output")
                st.text(st.session_state["captured_output"])

if __name__ == "__main__":
    show()
