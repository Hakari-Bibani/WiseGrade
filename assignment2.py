import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
from streamlit_folium import st_folium
import traceback
import sys


def show():
    st.title("Assignment 2: Earthquake Data Analysis with Custom Scripts")

    # Section 1: Student ID
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")

        if submit_id_button:
            if student_id:
                st.success(f"Student ID {student_id} verified. Proceed to upload your script.")
            else:
                st.error("Please enter a valid Student ID.")

    # Section 2: Upload User Script
    st.header("Step 2: Upload Your Script")
    uploaded_script = st.file_uploader("Upload your Google Colab Python script (.py)", type="py")

    if uploaded_script:
        st.session_state["run_success"] = False
        st.session_state["map_object"] = None
        st.session_state["bar_chart"] = None
        st.session_state["text_summary"] = None

        # Read and execute the user script
        script_code = uploaded_script.read().decode("utf-8")

        # Capture outputs
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        try:
            # Create a local context for execution
            local_context = {}

            # Execute the script
            exec(script_code, {}, local_context)
            st.session_state["run_success"] = True

            # Extract the outputs
            map_object = next(
                (obj for obj in local_context.values() if isinstance(obj, folium.Map)), None
            )
            if map_object:
                st.session_state["map_object"] = map_object

            plt_figure = next(
                (obj for obj in local_context.values() if isinstance(obj, plt.Figure)), None
            )
            if plt_figure:
                buffer = BytesIO()
                plt_figure.savefig(buffer, format="png")
                buffer.seek(0)
                st.session_state["bar_chart"] = buffer

            dataframe_object = next(
                (obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None
            )
            if dataframe_object is not None:
                st.session_state["text_summary"] = dataframe_object

            st.success("Script executed successfully! Check the outputs below.")

        except Exception as e:
            st.error(f"An error occurred while running the script: {e}")
            st.text(traceback.format_exc())
        finally:
            sys.stdout = old_stdout

    # Section 3: Display Outputs
    if st.session_state.get("run_success"):
        st.header("Step 3: Outputs")

        # Display the HTML map
        if st.session_state.get("map_object"):
            st.subheader("Interactive Map")
            st_folium(st.session_state["map_object"], width=700, height=500)

        # Display the bar chart
        if st.session_state.get("bar_chart"):
            st.subheader("Bar Chart")
            st.image(st.session_state["bar_chart"], use_column_width=True)

        # Display the text summary
        if st.session_state.get("text_summary") is not None:
            st.subheader("Text Summary")
            df = st.session_state["text_summary"]
            st.dataframe(df)

    # Section 4: Submission
    st.header("Step 4: Submit Your Work")
    if st.button("Submit Assignment"):
        if st.session_state.get("run_success"):
            st.success("Assignment submitted successfully!")
        else:
            st.error("Please ensure your script runs successfully before submission.")


if __name__ == "__main__":
    show()
