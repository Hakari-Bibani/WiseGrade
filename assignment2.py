import streamlit as st
from style2 import set_page_style

def show():
    # Apply the page style (from style2.py)
    set_page_style()
    
    st.title("Assignment 2: Earthquake Data Visualization")

    # ---- Student ID Section ----
    st.markdown("### Please Enter Your Student ID")
    st.markdown("*(Use the **same Student ID** generated in Assignment 1.)*")
    
    # We use a form to group the submission logic (including "Analyze" and "Submit" buttons)
    with st.form("assignment2_form", clear_on_submit=False):
        student_id = st.text_input("Student ID", value="")
        
        # ---- Tabs: Assignment Details & Grading Details ----
        tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])
        
        # ---- TAB 1: Assignment Details ----
        with tab1:
            st.markdown("""
            ## Assignment Details

            In this assignment, you will write a Python script that **fetches real-time earthquake data** from the USGS Earthquake API, processes the data to filter earthquakes with a **magnitude greater than 4.0**, and **plots the earthquake locations** on a map.

            Additionally, you will **calculate the number of earthquakes** in different magnitude ranges and present the results visually.

            **API Reference**:  
            [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/)  
            - **Base URL**: `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=YYYY-MM-DD&endtime=YYYY-MM-DD`
            - Replace the `YYYY-MM-DD` with appropriate dates.

            **Task Requirements**:
            1. **Use the USGS Earthquake API** to fetch data for the date range **January 2nd, 2025**, to **January 9th, 2025**.
            2. Filter the data to include **only earthquakes with a magnitude > 4.0**.
            3. Create an **interactive map** showing the locations of the filtered earthquakes.
                - Markers in different colors based on their magnitude range:
                  - **Green** for magnitude 4–5
                  - **Yellow** for magnitude 5–5.5
                  - **Red** for magnitude **> 5.5**
                - Popups showing **magnitude, location, and time**.
            4. A **bar chart** (`.png`) showing the frequency of earthquakes in the ranges:
               - 4.0–4.5, 4.5–5.0, and **>5.0**.
            5. A **text summary** (as CSV or similar) with the following:
               - Total number of earthquakes (magnitude >4.0).
               - Average, maximum, and minimum magnitudes (to two decimals).
               - Number of earthquakes in each magnitude range (e.g., 4–5, 5–6, 6+).

            **Python Libraries**:
            - `folium` for the map.
            - `matplotlib` or `seaborn` for the bar chart.
            - `requests` or `urllib` for API calls.
            - `pandas` for data processing.

            **Expected Output**:
            1. A **map** (`.html`)
            2. A **bar chart** (`.png`)
            3. A **text summary** (CSV or text)

            ---
            """)
        
        # ---- TAB 2: Grading Details ----
        with tab2:
            st.markdown("""
            ## Grading Details

            **1. Library Imports (10 Points)**
            - Using `folium` for the map: 2 points
            - Using `matplotlib` or `seaborn` for the bar chart: 2 points
            - Using `requests` or `urllib` for API calls: 2 points
            - Points for additional correct/clean setup: 4 points

            *(Additional grading criteria like code structure, map visualization, etc., can be added here as needed.)*
            """)

        # ---- Code Submission Area ----
        st.markdown("### Paste Your Code Below")

        # Light blue background for code area
        code_input_style = """
            <style>
            .code-input {
                background-color: #f0f8ff; 
                padding: 10px; 
                border-radius: 5px;
            }
            </style>
        """
        st.markdown(code_input_style, unsafe_allow_html=True)
        code_input = st.text_area(
            "",
            height=200,
            key="assignment2_code",
            placeholder="Paste your Python code here..."
        )

        # ---- Analyze Button ----
        analyze_button = st.form_submit_button("Analyze")

        st.markdown("---")

        # ---- File Uploads for Map, Bar Chart, and Summary ----
        st.markdown("### Upload Your Files")
        map_file = st.file_uploader("Upload the map (HTML file):", type=["html"])
        barchart_file = st.file_uploader("Upload the bar chart (PNG file):", type=["png"])
        summary_file = st.file_uploader("Upload the text summary (CSV/TXT):", type=["csv", "txt"])

        st.markdown("---")

        # ---- Submit Button ----
        submit_button = st.form_submit_button("Submit")

        # ---- Logic after form submission ----
        if submit_button:
            # Here you can add your logic to check if the Student ID is valid (e.g., query Google Sheets)
            # If valid, proceed to record the submission; if not, show an error message.
            if not student_id:
                st.error("Please enter a valid Student ID before submitting.")
            else:
                # Placeholder for your Student ID check logic
                # e.g., if check_student_id_in_google_sheet(student_id):
                #           st.success("Submission successful!")
                #       else:
                #           st.error("Invalid Student ID. Please check and try again.")
                st.info("Submission button clicked. (Integrate your Student ID validation logic here.)")

        if analyze_button:
            # Here you might implement code analysis, syntax checks, or any preliminary grading steps
            if not student_id:
                st.error("Please enter a valid Student ID before analyzing.")
            else:
                st.info("Analyze button clicked. (Add your code analysis logic here.)")
