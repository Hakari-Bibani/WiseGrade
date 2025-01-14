import streamlit as st
import folium
import traceback
import sys
from io import StringIO
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

def preprocess_code(user_code):
    """
    Preprocess the user-provided code to remove unsupported commands like `!pip install`.
    """
    filtered_lines = []
    for line in user_code.splitlines():
        # Skip lines that start with '!' or contain invalid shell commands
        if line.strip().startswith("!") or line.strip().startswith("%"):
            continue
        filtered_lines.append(line)
    return "\n".join(filtered_lines)

def extract_main_points(local_context):
    """Extract main points (map, bar chart, text summary) from the executed script."""
    map_object = next((obj for obj in local_context.values() if isinstance(obj, folium.Map)), None)
    bar_chart = next((obj for obj in local_context.values() if isinstance(obj, plt.Figure)), None)
    text_summary = next((obj for obj in local_context.values() if isinstance(obj, str) and len(obj) < 1000), None)
    return map_object, bar_chart, text_summary

def show():
    # Apply custom page style
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
        unsafe_allow_html=True,
    )

    st.title("Assignment 2: User Script Execution")
    st.header("Paste Your Code Below")

    # Text area for user-provided script
    code = st.text_area("Paste your Python script here", height=300)

    # Initialize session state variables
    if "run_success" not in st.session_state:
        st.session_state["run_success"] = False
    if "map_object" not in st.session_state:
        st.session_state["map_object"] = None
    if "bar_chart" not in st.session_state:
        st.session_state["bar_chart"] = None
    if "text_summary" not in st.session_state:
        st.session_state["text_summary"] = None

    if st.button("Run Code"):
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["text_summary"] = None

        # Preprocess the user code to remove invalid commands
        processed_code = preprocess_code(code)

        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Execute the preprocessed code
            local_context = {}
            exec(processed_code, {}, local_context)

            # Extract main points
            map_object, bar_chart, text_summary = extract_main_points(local_context)

            # Store outputs in session state
            st.session_state["map_object"] = map_object
            st.session_state["bar_chart"] = bar_chart
            st.session_state["text_summary"] = text_summary

            st.session_state["run_success"] = True
            st.success("Code executed successfully!")
        except Exception as e:
            st.error("An error occurred while executing the code:")
            st.error(traceback.format_exc())
        finally:
            # Restore stdout
            sys.stdout = old_stdout

    # Display Outputs
    if st.session_state["run_success"]:
        st.markdown("## Results")
        if st.session_state["map_object"]:
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["bar_chart"]:
            st.markdown("### 📊 Bar Chart")
            st.pyplot(st.session_state["bar_chart"])

        if st.session_state["text_summary"]:
            st.markdown("### 📄 Text Summary")
            st.text(st.session_state["text_summary"])

if __name__ == "__main__":
    show()
