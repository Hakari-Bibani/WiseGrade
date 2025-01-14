import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from streamlit_folium import st_folium
import traceback
import sys


def show():
    # Apply the custom page style
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
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "dataframe_object" not in st.session_state:
        st.session_state["dataframe_object"] = None
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None
    if "captured_output" not in st.session_state:
        st.session_state["captured_output"] = ""

    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Assignment Description
    st.header("Assignment Details")
    st.markdown("""
    ### Objective
    Write a Python script that fetches real-time earthquake data from the USGS Earthquake API, filters earthquakes with a magnitude greater than 4.0, and visualizes the data on a map and as a bar chart.
    """)

    # Section 2: Code Editor
    st.header("Step 1: Paste Your Code Below")
    code = st.text_area("Paste your Python script here", height=300)

    # Run the user's code
    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["dataframe_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["captured_output"] = ""

        # Redirect stdout
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Execute the user-provided script
            local_context = {}
            exec(code, {}, local_context)
            st.session_state["run_success"] = True
            st.session_state["captured_output"] = new_stdout.getvalue()

            # Detect Folium map
            st.session_state["map_object"] = next(
                (obj for obj in local_context.values() if isinstance(obj, folium.Map)),
                None
            )

            # Detect a Pandas DataFrame
            st.session_state["dataframe_object"] = next(
                (obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)),
                None
            )

            # Detect a matplotlib figure
            for obj in local_context.values():
                if isinstance(obj, plt.Figure):
                    buffer = BytesIO()
                    obj.savefig(buffer, format="png")
                    buffer.seek(0)
                    st.session_state["bar_chart"] = buffer
                    break

            st.success("Code executed successfully!")
        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.text(traceback.format_exc())
        finally:
            sys.stdout = old_stdout

    # Section 3: Display Outputs
    st.header("Step 2: Visualize Your Outputs")
    
    if st.session_state["run_success"]:
        if st.session_state["map_object"]:
            st.markdown("### 🗺️ Earthquake Map")
            st_folium(st.session_state["map_object"], width=700, height=500)
        else:
            st.warning("No map detected in your script.")

        if st.session_state["bar_chart"]:
            st.markdown("### 📊 Earthquake Frequency by Magnitude")
            st.image(st.session_state["bar_chart"], caption="Earthquake Frequency by Magnitude Range")
        else:
            st.warning("No bar chart detected in your script.")

        if st.session_state["dataframe_object"] is not None:
            st.markdown("### 📋 Summary of Earthquake Data")
            st.dataframe(st.session_state["dataframe_object"])
        else:
            st.warning("No summary data detected in your script.")
    else:
        st.warning("Please run your code to view the outputs.")

    # Section 4: Submit Assignment
    st.header("Step 3: Submit Your Assignment")
    if st.button("Submit Assignment"):
        if st.session_state["run_success"]:
            st.success("Assignment submitted successfully! Your outputs have been recorded.")
        else:
            st.error("Please run your code successfully before submitting.")


if __name__ == "__main__":
    show()
