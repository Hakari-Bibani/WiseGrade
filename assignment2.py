# assignment2.py
import streamlit as st
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet
import traceback
import folium
import pandas as pd
import matplotlib.pyplot as plt
import sys
from io import StringIO

# Set the page style
set_page_style()

# Custom display hook to capture the last evaluated expression
class OutputCapture:
    def __init__(self):
        self.last_output = None

    def __call__(self, value):
        self.last_output = value

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Student Information Form
    with st.form("student_form", clear_on_submit=False):
        # Display Student ID (generated in Assignment 1)
        student_id = st.text_input("Student ID", key="student_id", help="Enter the Student ID generated in Assignment 1.")
        
        # Tabs for assignment and grading details
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown("""
            ### Instructions for Code Submission
            1. Fetch earthquake data from the USGS API.
            2. Filter earthquakes with magnitude > 4.0.
            3. Create a Folium map.
            4. Create a DataFrame with earthquake statistics.
            5. Create a bar chart.
            6. Paste your code below and click **Run** to see the outputs.
            """)

        # Code Submission Area
        code_input = st.text_area("**📝 Paste Your Code Here**", height=300, help="Paste your Python code here.")

        # Form Submit Buttons
        run_button = st.form_submit_button("Run")
        submit_button = st.form_submit_button("Submit")

    # Execute the user's code
    if run_button and code_input:
        try:
            # Create a local dictionary to capture code execution results
            local_context = {}
            output_capture = OutputCapture()
            sys.displayhook = output_capture

            # Redirect stdout to capture print statements
            stdout_capture = StringIO()
            sys.stdout = stdout_capture

            # Execute the user's code
            exec(code_input, {}, local_context)

            # Restore stdout and display hook
            sys.stdout = sys.__stdout__
            sys.displayhook = sys.__displayhook__

            # Capture the last evaluated expression
            last_output = output_capture.last_output

            # Display outputs
            if isinstance(last_output, folium.Map):
                st.success("Map generated successfully!")
                st.markdown("### 🗺️ Generated Map")
                st.components.v1.html(last_output._repr_html_(), height=500)
            elif isinstance(last_output, pd.DataFrame):
                st.markdown("### 📊 Earthquake Statistics")
                st.write(last_output)
            elif isinstance(last_output, plt.Figure):
                st.markdown("### 📈 Earthquake Frequency by Magnitude Range")
                st.pyplot(last_output)
            else:
                st.warning("No supported output found in the code (expected: Folium map, DataFrame, or Matplotlib plot).")

            # Display captured stdout (print statements)
            stdout_output = stdout_capture.getvalue()
            if stdout_output:
                st.markdown("### 📝 Console Output")
                st.text(stdout_output)

        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())

    # Submit and grade
    if submit_button and code_input:
        if student_id:
            grade = grade_assignment(code_input)
            update_google_sheet("N/A", "N/A", student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please enter your Student ID to submit your assignment.")

# Entry point for Streamlit
def main():
    show()

# Run the app
if __name__ == "__main__":
    main()
