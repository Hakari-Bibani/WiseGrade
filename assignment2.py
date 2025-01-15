import streamlit as st
import traceback
from io import StringIO
from streamlit_folium import st_folium
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Student ID Input
    st.header("Step 1: Enter Your Student ID")
    with st.form("student_id_form", clear_on_submit=False):
        student_id = st.text_input("Enter Your Student ID", key="student_id")
        submit_id_button = st.form_submit_button("Verify Student ID")
        if submit_id_button:
            if student_id:  # Verify student ID logic (placeholder)
                st.success(f"Student ID {student_id} verified. You may proceed.")
            else:
                st.error("Please provide a valid Student ID.")

    # Section 2: Paste Code
    st.header("Step 2: Paste Your Code")
    code = st.text_area("Paste your Python code here", height=300, key="code_cell")

    # Section 3: Upload Files
    st.header("Step 3: Upload Your Outputs")
    uploaded_html = st.file_uploader("Upload the HTML map file", type=["html"], key="html_upload")
    uploaded_png = st.file_uploader("Upload the PNG bar chart", type=["png"], key="png_upload")
    uploaded_csv = st.file_uploader("Upload the CSV summary", type=["csv"], key="csv_upload")

    # Section 4: Check Submission
    if st.button("Check Submission"):
        st.header("Submission Results")
        results = []

        # Process uploaded HTML
        if uploaded_html:
            try:
                html_content = uploaded_html.getvalue().decode("utf-8")
                soup = BeautifulSoup(html_content, "html.parser")
                markers = soup.find_all("marker")
                if markers:
                    results.append("✅ Map contains markers for earthquakes.")
                else:
                    results.append("❌ Map does not contain any markers.")
                # Additional checks for color coding and popups could go here
            except Exception as e:
                results.append(f"❌ Error processing HTML file: {e}")
        else:
            results.append("❌ No HTML map file uploaded.")

        # Process uploaded PNG
        if uploaded_png:
            try:
                # Placeholder for bar chart comparison logic
                # Compare uploaded chart with reference chart here
                results.append("✅ PNG bar chart uploaded successfully.")
            except Exception as e:
                results.append(f"❌ Error processing PNG bar chart: {e}")
        else:
            results.append("❌ No PNG bar chart uploaded.")

        # Process uploaded CSV
        if uploaded_csv:
            try:
                summary_df = pd.read_csv(uploaded_csv)
                # Placeholder for CSV validation logic
                results.append("✅ CSV summary uploaded successfully.")
            except Exception as e:
                results.append(f"❌ Error processing CSV summary: {e}")
        else:
            results.append("❌ No CSV summary uploaded.")

        # Display results
        for result in results:
            st.write(result)

    # Section 5: Run and Grade Code
    st.header("Step 4: Run Your Code")
    if st.button("Run Code"):
        if not code:
            st.error("Please paste your code before running.")
        else:
            st.session_state["captured_output"] = ""
            old_stdout = StringIO()
            try:
                exec(code, {})
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state["captured_output"] = traceback.format_exc()
            finally:
                st.text_area("Captured Output", st.session_state["captured_output"], height=200)

    # Section 6: Submit Assignment
    st.header("Step 5: Submit Your Assignment")
    submit_button = st.button("Submit Assignment")
    if submit_button:
        if not code or not uploaded_html or not uploaded_png or not uploaded_csv:
            st.error("Please ensure all fields are completed (code, HTML, PNG, CSV) before submission.")
        else:
            st.success("Assignment submitted successfully! Your outputs will be graded.")

if __name__ == "__main__":
    show()
