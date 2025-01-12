# assignment2.py
import streamlit as st
from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet
import traceback
import folium
import pandas as pd

# Set the page style
set_page_style()

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
            3. Create a Folium map and assign it to a variable named `earthquake_map`.
            4. Create a DataFrame with earthquake statistics and assign it to a variable named `earthquakes`.
            5. Paste your code below and click **Run** to see the outputs.
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
            exec(code_input, {}, local_context)

            # Search for outputs
            map_object = find_folium_map(local_context)
            dataframe_object = find_dataframe(local_context)

            # Display outputs
            if map_object:
                st.success("Map generated successfully!")
                st.markdown("### 🗺️ Generated Map")
                st.components.v1.html(map_object._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the code output.")

            if dataframe_object is not None:
                st.markdown("### 📊 Earthquake Statistics")
                st.write(dataframe_object)
            else:
                st.warning("No DataFrame with earthquake statistics found in the code output.")

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

# Helper functions
def find_folium_map(local_context):
    """Search for a Folium map object in the local context."""
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            return var_value
    return None

def find_dataframe(local_context):
    """Search for a Pandas DataFrame or similar in the local context."""
    for var_name, var_value in local_context.items():
        if isinstance(var_value, pd.DataFrame):
            return var_value
    return None

# Entry point for Streamlit
def main():
    show()

# Run the app
if __name__ == "__main__":
    main()
