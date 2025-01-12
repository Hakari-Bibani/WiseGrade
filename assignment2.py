import streamlit as st
from style2 import set_page_style_2
from Record.google_sheet import fetch_student_ids  # You need to implement this to return valid student IDs

def show():
    # Apply custom page style
    set_page_style_2()
    
    st.title("Assignment 2: Real-time Earthquake Data Visualization")

    # Fetch valid student IDs from Google Sheet
    # This function should return a list of valid IDs (strings)
    try:
        student_ids = fetch_student_ids()
    except Exception as e:
        st.error(f"Could not fetch student IDs. Error: {e}")
        student_ids = []

    # Student Form for Assignment 2
    with st.form("student_form_2", clear_on_submit=False):
        # Allow user to select only valid student IDs from assignment1
        selected_student_id = st.selectbox("Select Your Student ID", options=student_ids)

        # Two tabs for the assignment details and grading details
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

        with tab1:
            st.markdown(
                """
                **In this assignment, you will write a Python script that fetches real-time earthquake data from the USGS Earthquake API, processes the data to filter earthquakes with a magnitude greater than 4.0, and plots the earthquake locations on a map. Additionally, you will calculate the number of earthquakes in different magnitude ranges and present the results visually.**

                **May be you need this API:**  
                [USGS Earthquake API Docs](https://earthquake.usgs.gov/fdsnws/event/1/)  
                The API URL is:  
                ```
                https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=YYYY-MM-DD&endtime=YYYY-MM-DD
                ```
                Replace `YYYY-MM-DD` with the date range **January 2nd, 2025, to January 9th, 2025**.

                **Task Requirements:**
                - Use the USGS Earthquake API to fetch data for the date range January 2nd, 2025, to January 9th, 2025.
                - The data will be in GeoJSON format, containing earthquake location (latitude, longitude), magnitude, and time (in readable format).
                - Filter the data to include only earthquakes with a magnitude **greater than 4.0**.
                - Create an interactive map that shows the locations of the filtered earthquakes.
                - Mark the earthquake locations on the map with markers, using different colors based on their magnitude:
                  - **Green** for magnitude 4-5
                  - **Yellow** for 5-5.5
                  - **Red** for 5.5+
                - Add popups to display additional information about each earthquake (magnitude, location, and time).
                - Create a **(.png)** visualization of earthquake frequency by magnitude, represented as a bar chart, within the following magnitude ranges: 
                  - `4.0-4.5`, `4.5-5.0`, and `> 5.0`.
                - Generate a **text summary as CSV** (Express values to two decimal places) that includes:
                  - Total number of earthquakes with magnitude > 4.0.
                  - Average, maximum, and minimum magnitudes.
                  - Number of earthquakes in each magnitude range (4-5, 5-6, 6+).

                **Python Libraries You Will Use**
                - `folium` for the map.
                - `matplotlib` or `seaborn` for the bar chart.
                - `requests` or `urllib` for API calls.
                - `pandas` for data processing.

                **Expected Output:**
                1. An interactive map
                2. A bar chart
                3. A text summary
                """
            )

        with tab2:
            st.markdown(
                """
                **1. Library Imports (10 Points)**
                - Points Allocation:
                  - `folium` for the map: **2 points**
                  - `matplotlib` or `seaborn` for the bar chart: **2 points**
                  - `requests` or `urllib` for API calls: **2 points**
                - (Additional breakdown can be added here as needed)
                """
            )

        # Code submission area (Light-blue background is applied by style2.py)
        st.markdown("**Paste Your Code Here**")
        code_input = st.text_area("Your Python Code", height=250, key="assignment2_code")

        st.markdown("---")

        # File uploaders: HTML (map), PNG (barchart), Text summary
        st.markdown("**Upload Your Outputs**")
        uploaded_html = st.file_uploader("Upload the HTML file (map output)", type=["html"], key="map_html")
        uploaded_png = st.file_uploader("Upload the PNG file (barchart)", type=["png"], key="barchart_png")
        uploaded_text = st.file_uploader("Upload the text summary (CSV)", type=["csv", "txt"], key="text_summary")

        # Action buttons
        analyze_button = st.form_submit_button("Analyze")
        submit_button = st.form_submit_button("Submit")

    # Handle Analyze action
    if analyze_button:
        st.info("Analyzing your code... (Placeholder for your actual analysis logic)")

    # Handle Submit action
    if submit_button:
        if selected_student_id:
            st.success(f"Your submission for Student ID: {selected_student_id} has been received.")
            # TODO: Implement logic to save the student's code, files, and grade to Google Sheet
        else:
            st.error("Please select a valid Student ID before submitting.")
