import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import sys
from streamlit_folium import st_folium
from utils.style1 import set_page_style

def generate_student_id(name, email):
    """Generate a unique student ID based on name and email."""
    import random
    import string
    if name and email:
        random_numbers = ''.join(random.choices(string.digits, k=4))
        random_letter = random.choice(string.ascii_uppercase)
        return random_numbers + random_letter
    return "N/A"

def show():
    # Apply the custom page style
    set_page_style()

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

    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Student Information Form
    st.header("Step 1: Enter Your Details")
    with st.form("student_form", clear_on_submit=False):
        full_name = st.text_input("Full Name", key="full_name")
        email = st.text_input("Email", key="email")

        generate_id_button = st.form_submit_button("Generate Student ID")

        if generate_id_button:
            if full_name and email:
                student_id = generate_student_id(full_name, email)
                st.success(f"Student ID generated: {student_id}")
            else:
                st.error("Please provide both Full Name and Email to generate a Student ID.")

    # Section 2: Assignment and Grading Details
    st.header("Step 2: Review Assignment Details")
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        ### Objective
        In this assignment, you will write a Python script to fetch real-time earthquake data from the USGS Earthquake API, process the data to filter earthquakes with a magnitude greater than 4.0, and plot the earthquake locations on a map. Additionally, you will calculate the number of earthquakes in different magnitude ranges and present the results visually.

        ### Task Requirements:
        1. Use the USGS Earthquake API to fetch data for the date range January 2nd, 2025, to January 9th, 2025.
        2. Filter the data to include only earthquakes with a magnitude greater than 4.0.
        3. Create an interactive map showing the locations of the filtered earthquakes.
        4. Mark the earthquake locations on the map with markers, using different colors based on their magnitude.
        5. Add popups to display additional information about each earthquake (magnitude, location, and time).
        6. Generate a bar chart showing the frequency of earthquakes by magnitude range.
        7. Provide a text summary of the earthquake data.
        """)

    with tab2:
        st.markdown("""
        ### Detailed Grading Breakdown
        #### 1. Code Structure and Implementation (30 points)
        - **Library Imports (5 points):**
            - Checks if the required libraries (`folium`, `matplotlib`, `pandas`, `requests`) are imported.
        - **API Data Fetching (10 points):**
            - Checks if the API is called correctly and data is fetched.
        - **Code Execution (10 points):**
            - Checks if the code runs without errors.
        - **Code Quality (5 points):**
            - **Variable Naming:** Deducted if single-letter variables are used.
            - **Spacing:** Deducted if improper spacing is found.
            - **Comments:** Deducted if no comments are present.
            - **Code Organization:** Deducted if no blank lines are used for separation.

        #### 2. Map Visualization (30 points)
        - **Map Generation (10 points):**
            - Checks if the `folium.Map` is correctly initialized.
        - **Markers (10 points):**
            - Checks if markers are added to the map for each earthquake.
        - **Popups (10 points):**
            - Checks if popups are added to the markers.

        #### 3. Bar Chart and Text Summary (40 points)
        - **Bar Chart (20 points):**
            - Checks if the bar chart is generated correctly.
        - **Text Summary (20 points):**
            - Checks if the text summary is accurate and formatted correctly.
        """)

    # Section 3: Code Submission and Output
    st.header("Step 3: Submit and Run Your Code")
    code_input = st.text_area("**📝 Paste Your Code Here**", height=300)

    # Run Code Button
    run_button = st.button("Run Code", key="run_code_button")
    if run_button and code_input:
        st.session_state["run_success"] = False
        st.session_state["captured_output"] = ""
        try:
            # Redirect stdout to capture print statements
            captured_output = StringIO()
            sys.stdout = captured_output

            # Execute the user's code in a controlled environment
            local_context = {}
            exec(code_input, {}, local_context)

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Capture printed output
            st.session_state["captured_output"] = captured_output.getvalue()

            # Look for specific outputs (folium.Map, matplotlib plot, pandas.DataFrame)
            map_object = None
            bar_chart = None
            text_summary = None

            # Search for folium.Map
            for var_name, var_value in local_context.items():
                if isinstance(var_value, folium.Map):
                    map_object = var_value
                elif isinstance(var_value, plt.Figure):
                    bar_chart = var_value
                elif isinstance(var_value, pd.DataFrame):
                    text_summary = var_value

            # Store outputs in session state
            st.session_state["map_object"] = map_object
            st.session_state["bar_chart"] = bar_chart
            st.session_state["text_summary"] = text_summary

            # Mark the run as successful
            st.session_state["run_success"] = True

        except Exception as e:
            sys.stdout = sys.__stdout__
            st.error(f"An error occurred while running your code: {e}")

    # Display Outputs
    if st.session_state["run_success"]:
        st.markdown("### 📄 Captured Output")
        if st.session_state["captured_output"]:
            st.text(st.session_state["captured_output"])
        else:
            st.write("No text output captured.")

        if st.session_state["map_object"]:
            st.markdown("### 🗺️ Map Output")
            st_folium(st.session_state["map_object"], width=700, height=500)

        if st.session_state["bar_chart"]:
            st.markdown("### 📊 Bar Chart Output")
            st.pyplot(st.session_state["bar_chart"])

        if st.session_state["text_summary"] is not None:
            st.markdown("### 📝 Text Summary")
            st.dataframe(st.session_state["text_summary"])

    # Submit Code Button
    submit_button = st.button("Submit Code", key="submit_code_button")
    if submit_button:
        if not st.session_state.get("run_success", False):
            st.error("Please run your code successfully before submitting.")
        elif full_name and email:
            from grades.grade2 import grade_assignment
            from Record.google_sheet import update_google_sheet

            grade = grade_assignment(code_input)
            student_id = generate_student_id(full_name, email)
            update_google_sheet(full_name, email, student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please ensure Full Name and Email are entered to submit.")

# Entry point for Streamlit
if __name__ == "__main__":
    show()
