import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from streamlit_folium import st_folium
import traceback
import sys

def show():
    # Apply a custom page style
    st.markdown("""
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
        """, unsafe_allow_html=True)

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None
    if "text_summary" not in st.session_state:
        st.session_state["text_summary"] = None
    if "captured_output" not in st.session_state:
        st.session_state["captured_output"] = ""

    st.title("Assignment 2: Streamlit Integration for Student Scripts")

    # Step 1: User Script Input
    st.header("Step 1: Paste Your Script")
    user_script = st.text_area("Paste your Python script below", height=300)

    # Step 2: Run the Script
    if st.button("Run Script"):
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["text_summary"] = None
        st.session_state["captured_output"] = ""

        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Prepare execution context
            local_context = {}

            # Execute the student's script
            exec(user_script, {}, local_context)

            # Capture outputs
            st.session_state["captured_output"] = new_stdout.getvalue()
            st.session_state["run_success"] = True

            # Extract main points from the execution context
            # 1. Extract the Folium map object
            st.session_state["map_object"] = next(
                (obj for obj in local_context.values() if isinstance(obj, folium.Map)), None
            )

            # 2. Extract the Matplotlib/Seaborn bar chart
            for obj in local_context.values():
                if isinstance(obj, plt.Figure):
                    buf = BytesIO()
                    obj.savefig(buf, format="png")
                    buf.seek(0)
                    st.session_state["bar_chart"] = buf
                    break

            # 3. Extract the text summary as a DataFrame
            st.session_state["text_summary"] = next(
                (obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None
            )

            st.success("Script executed successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state["captured_output"] = traceback.format_exc()
        finally:
            sys.stdout = old_stdout

    # Step 3: Display Results
    if st.session_state["run_success"]:
        st.header("Results")

        # Display the Folium map
        if st.session_state["map_object"]:
            st.subheader("Map Visualization")
            st_folium(st.session_state["map_object"], width=700, height=500)

        # Display the bar chart
        if st.session_state["bar_chart"]:
            st.subheader("Bar Chart")
            st.image(st.session_state["bar_chart"], use_column_width=True)

        # Display the text summary
        if st.session_state["text_summary"] is not None:
            st.subheader("Text Summary")
            st.dataframe(st.session_state["text_summary"])
        else:
            st.info("No DataFrame was found in the script.")

    # Step 4: Debugging Info (Optional)
    if st.checkbox("Show Debugging Information"):
        st.text_area("Captured Output", st.session_state["captured_output"], height=200)


if __name__ == "__main__":
    show()
