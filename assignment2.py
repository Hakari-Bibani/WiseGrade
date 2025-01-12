import streamlit as st
import traceback
# Import your style2.py (to be created)
# from utils.style2 import set_page_style

# Import your grading and record modules (to be created or adapted)
# from grades.grade2 import grade_assignment
# from Record.google_sheet import update_google_sheet

import folium
import pandas as pd


def find_folium_map(local_context):
    """
    Search for a Folium map object in the local context.
    """
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            return var_value
    return None


def find_dataframe(local_context):
    """
    Search for a Pandas DataFrame or similar in the local context.
    """
    for var_name, var_value in local_context.items():
        if isinstance(var_value, pd.DataFrame):
            return var_value
    return None


def show():
    """
    Renders the Streamlit UI for Assignment 2.
    """
    # Optional: Set page style from style2.py
    # set_page_style()

    st.title("Assignment 2: Earthquake Data Processing")

    # Display Student ID (read-only) - assume it's stored in st.session_state by assignment1.py
    student_id = st.text_input("Student ID", 
                               value=st.session_state.get("student_id", "N/A"), 
                               disabled=True)

    # Create Tabs
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown(
            """
            ### Objective
            In this assignment, you will write a Python script that fetches real-time earthquake data 
            from the USGS Earthquake API, processes the data to filter earthquakes with a magnitude 
            greater than 4.0, and plots the earthquake locations on a map. Additionally, you will 
            calculate the number of earthquakes in different magnitude ranges and present the results visually.

            **May be you need this API:**  [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/).

            **API URL Example:**
            ```
            https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=YYYY-MM-DD&endtime=YYYY-MM-DD
            ```
            Replace `YYYY-MM-DD` with the appropriate dates.

            **Task Requirements:**
            - Use the USGS Earthquake API to fetch data for the date range **January 2nd, 2025** to **January 9th, 2025**.
            - Filter the data to include only earthquakes with a magnitude greater than **4.0**.
            - Create an interactive map that shows the locations of the filtered earthquakes.
            - Mark earthquake locations with **different colors** based on magnitude:
              - Green for magnitude 4.0-5.0
              - Yellow for 5.0-5.5
              - Red for 5.5+
            - Add **popups** to display additional information (magnitude, location, and time).
            - Create a **bar chart** to visualize earthquake frequency by magnitude range:
              - 4.0-4.5, 4.5-5.0, and greater than 5.0.
            - Provide a **text summary** (as CSV) that includes:
              - Total number of earthquakes with magnitude > 4.0
              - Average, maximum, and minimum magnitudes (rounded to 2 decimals)
              - Number of earthquakes in each magnitude range (4.0-4.5, 4.5-5.0, 5.0+)
            """
        )

    with tab2:
        st.markdown(
            """
            ### Grading Details

            **1. Library Imports (10 Points)**
            - **Points Allocation**:
              - folium for the map: 2 points  
              - matplotlib or seaborn for the bar chart: 2 points  
              - requests or urllib for API calls: 2 points  
              - pandas for data processing: 2 points  
              - Proper import organization and no unused libraries: 2 points
            - **Deductions**:
              - Missing any required library: -2 points per library  
              - Unnecessary libraries imported: -1 point per library

            **2. Code Quality (20 Points)**
            - **Variable Naming (5 Points)**:  
              - Descriptive variable names: 5 points
            - **Spacing (5 Points)**:  
              - Proper spacing after operators: 5 points
            - **Comments (5 Points)**:  
              - Comments explaining each major step: 5 points
            - **Code Organization (5 Points)**:  
              - Logical separation of code blocks with blank lines: 5 points

            **3. Fetching Data from the API (10 Points)**
            - **Points Allocation**:
              - Correct API URL with date range: 3 points
              - Successful data retrieval using requests or urllib: 3 points
              - Proper error handling: 4 points

            **4. Filtering Earthquakes (10 Points)**
            - **Points Allocation**:
              - Correct filtering of magnitudes > 4.0: 5 points
              - Proper extraction of data fields: 5 points

            **5. Map Visualization (20 Points)**
            - **Points Allocation**:
              - Map generation: 5 points  
              - Markers color-coded based on magnitude:
                - Green (4.0-5.0): 3 points  
                - Yellow (5.0-5.5): 3 points  
                - Red (5.5+): 3 points  
              - Popups:
                - Magnitude, Lat/Long, Time: total 6 points

            **6. Bar Chart (15 Points)**
            - **Points Allocation**:
              - Bar chart with correct magnitude ranges (4.0-4.5, 4.5-5.0, 5.0+)
              - Proper labeling (title, axes)

            **7. Text Summary (15 Points)**
            - **Points Allocation**:
              - Total earthquakes (> 4.0): 3 points  
              - Avg, max, min magnitude (2 decimals): 9 points  
              - Breakdown by magnitude range: 3 points  

            **8. Overall Execution (10 Points)**
            - **Points Allocation**:
              - No errors: 5 points  
              - Correct outputs: 5 points
            """
        )

    # Code Submission Area (light blue box style optional via CSS or style2.py)
    code_input = st.text_area(
        "Paste Your Code Here",
        height=300
    )

    # Action Buttons
    run_button = st.button("Run")
    submit_button = st.button("Submit")

    # Execute user code
    if run_button and code_input:
        try:
            local_context = {}
            exec(code_input, {}, local_context)

            # Try to find a Folium map in local context
            map_object = find_folium_map(local_context)
            if map_object:
                st.success("Map generated successfully!")
                st.markdown("### 🗺️Generated Map")
                st.components.v1.html(map_object._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the code output.")

            # Try to find a DataFrame (for summary or table)
            dataframe_object = find_dataframe(local_context)
            if dataframe_object is not None:
                st.markdown("### 📊Data / Summary")
                st.write(dataframe_object)
            else:
                st.warning("No DataFrame found in the code output.")

        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())

    # Submit and grade
    if submit_button and code_input:
        if student_id and student_id != "N/A":
            # grade = grade_assignment(code_input)
            # update_google_sheet("N/A for FullName", "N/A for Email", student_id, grade, "assignment_2")
            # st.success(f"Submission successful! Your grade: {grade}/100")

            # Placeholder message (since grade2.py not implemented yet)
            st.info("Grade submission feature is not yet implemented. This is a placeholder.")
        else:
            st.error("No valid Student ID found. Please check your Assignment 1 submission.")
