# assignment2.py

import streamlit as st
from utils.style2 import set_page_style
# from Record.google_sheet import get_student_ids  # <-- Implement or adapt this function to read Student IDs from Google Sheet
# from grades.grade2 import grade_assignment2      # <-- (Placeholder) For future grading logic

def get_student_ids():
    """
    Temporary placeholder function.
    In your actual code, implement or call an existing function
    that fetches all valid student IDs from the Google Sheet
    used in assignment1.
    """
    # Example (hardcoded) IDs for demonstration:
    return ["1234A", "5678B", "9012C"]

def show():
    # Set page style (we'll define style2.py separately)
    set_page_style()

    st.title("Assignment 2: Earthquake Data Analysis")

    # Fetch existing student IDs from Google Sheet (placeholder)
    student_ids = get_student_ids()

    # Student ID (read-only via dropdown of existing IDs)
    st.subheader("Select Your Student ID")
    selected_student_id = st.selectbox(
        "Only previously registered IDs are available",
        options=student_ids,
        help="Select the Student ID generated from Assignment 1"
    )

    # Two tabs for "Assignment Details" and "Grading Details"
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown(
            """
            **In this assignment**, you will write a Python script that fetches real-time earthquake data 
            from the USGS Earthquake API, processes the data to filter earthquakes with a magnitude greater 
            than 4.0, and plots the earthquake locations on a map. Additionally, you will calculate the number 
            of earthquakes in different magnitude ranges and present the results visually.
            
            **Maybe you need this API**: [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/).

            **API URL**:
            ```
            https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=YYYY-MM-DD&endtime=YYYY-MM-DD
            ```
            Replace `YYYY-MM-DD` with the appropriate dates.

            ### Task Requirements
            - Use the USGS Earthquake API to fetch data for **January 2nd, 2025, to January 9th, 2025**.
            - Filter data to include only **earthquakes with magnitude > 4.0**.
            - Create an **interactive map** showing locations of the filtered earthquakes:
                - Markers with **different colors** based on magnitude:
                  - Green for magnitude 4–5
                  - Yellow for magnitude 5–5.5
                  - Red for magnitude 5.5+
                - Popups to display magnitude, location, and time.
            - Create a **bar chart** (PNG) showing earthquake frequency by magnitude range:
              - 4.0–4.5
              - 4.5–5.0
              - > 5.0
            - Provide a **text summary** (CSV) with:
              - Total number of earthquakes with magnitude > 4.0
              - Average, maximum, and minimum magnitudes
              - Count of earthquakes in each magnitude range
            """
        )

    with tab2:
        st.markdown(
            """
            ### Grading Details
            
            **1. Library Imports (10 Points)**
            - folium for the map: **2 points**
            - matplotlib or seaborn for the bar chart: **2 points**
            - requests or urllib for API calls: **2 points**

            *(Additional grading criteria can be added here if needed.)*
            """
        )

    st.markdown("---")

    # Code Submission Area (with a light-blue background)
    # One way: use markdown + CSS
    st.markdown(
        """
        <div style="background-color: #E6F7FF; padding: 1rem; border-radius: 5px;">
            <strong>📝 Paste Your Code Here</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
    code_input = st.text_area(
        label="",
        placeholder="Paste your earthquake data analysis code here...",
        height=200
    )

    # Analyze button
    analyze_button = st.button("Analyze")

    # File upload areas
    st.markdown("**Upload Your Outputs**")
    uploaded_map_html = st.file_uploader(
        "Upload the HTML file for the map (exported from Folium)", 
        type=["html"]
    )
    uploaded_barchart = st.file_uploader(
        "Upload the PNG of the bar chart", 
        type=["png"]
    )
    uploaded_text_summary = st.file_uploader(
        "Upload the text summary (CSV)", 
        type=["csv"]
    )

    # Submit button
    submit_button = st.button("Submit")

    # Handle button clicks
    if analyze_button:
        st.info("Your code is being analyzed... (placeholder logic here)")
        # Here you might run or parse the code, do linting, etc.

    if submit_button:
        # Perform submission logic
        if not selected_student_id:
            st.error("Please select a valid Student ID before submitting.")
            return
        
        # Potentially, you’d call a grading function or store these results in Google Sheets
        st.success("Your assignment has been submitted successfully!")
        # e.g., grade_assignment2(...) or update_google_sheet(...)
