# assignment2.py
import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from streamlit_folium import st_folium
import traceback
import sys

def show():
    # Apply the custom page style
    st.markdown(

    # Section 3: Code Submission and Output
    st.header("Step 3: Submit Your Code")
    code_input = st.text_area("**\U0001F4DD Paste Your Code Here**", height=300)
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

    run_button = st.button("Run Code", key="run_code_button")
    submit_button = st.button("Submit Code", key="submit_code_button")
            captured_output = StringIO()
            sys.stdout = captured_output

            # Pre-import required libraries
            pre_imports = """
import requests
import pandas as pd
import folium
import matplotlib.pyplot as plt
from io import StringIO
"""
            # Combine pre-imports with user code
            exec_code = pre_imports + "\n" + code_input
            # Pre-import required libraries and inject into execution context
            exec_globals = {
                "__builtins__": __builtins__,
                "requests": __import__("requests"),
                "pd": pd,
                "folium": folium,
                "plt": plt,
                "StringIO": StringIO,
            }

            # Execute user code
            local_context = {}
            exec(exec_code, {}, local_context)
            exec(code_input, exec_globals)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Process outputs
            st.session_state["captured_output"] = captured_output.getvalue()
            st.session_state["map_object"] = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
            st.session_state["dataframe_object"] = next((obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None)
            st.session_state["map_object"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, folium.Map)), None)
            st.session_state["dataframe_object"] = next(
                (obj for obj in exec_globals.values() if isinstance(obj, pd.DataFrame)), None)
            st.session_state["bar_chart"] = plt.gcf() if plt.get_fignums() else None

            st.session_state["run_success"] = True
    # Display Outputs
    if st.session_state["run_success"]:
        if st.session_state["captured_output"]:
            st.markdown("### \U0001F4DA Captured Output")
            st.markdown("### 📜 Captured Output")
            st.text(st.session_state["captured_output"])

        if st.session_state["map_object"]:
            st.markdown("### \U0001F5FA Map Output")
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["bar_chart"]:
            st.markdown("### \U0001F4C8 Bar Chart Output")
            st.markdown("### 📊 Bar Chart Output")
            st.pyplot(st.session_state["bar_chart"])

        if st.session_state["dataframe_object"] is not None:
            st.markdown("### \U0001F4CA Data Summary")
            st.markdown("### 📑 Data Summary")
            st.dataframe(st.session_state["dataframe_object"])

    if submit_button:
        if st.session_state.get("run_success", False):
            st.success("Code submitted successfully! Your outputs have been recorded.")
            # Save submission logic here (e.g., Google Sheets or database)
        else:
            st.error("Please run your code successfully before submitting.")
