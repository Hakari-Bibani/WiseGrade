import streamlit as st
import pandas as pd
from io import StringIO
from grades.grade2 import grade_assignment
from Record.google_sheet import verify_student_id, update_google_sheet
import traceback


def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Verify Student ID
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Enter Your Student ID")

    if st.button("Verify Student ID"):
        if verify_student_id(student_id):  # Verifies if the ID exists in Google Sheets
            st.success(f"Student ID {student_id} verified. You may proceed.")
            st.session_state["id_verified"] = True
        else:
            st.error("Invalid Student ID. Please enter a valid ID.")

    if not st.session_state.get("id_verified", False):
        st.warning("You need to verify your Student ID to proceed.")
        st.stop()

    # Section 2: Code Editor
    st.header("Step 2: Write and Run Your Code")
    code = st.text_area("Paste your Python code here", height=300)

    # Section 3: Upload Files
    st.header("Step 3: Upload Your Outputs")
    uploaded_html = st.file_uploader("Upload your Map (HTML file)", type="html")
    uploaded_png = st.file_uploader("Upload your Bar Chart (PNG file)", type="png")
    uploaded_csv = st.file_uploader("Upload your Summary (CSV file)", type="csv")

    if st.button("Check Uploads"):
        if uploaded_html and uploaded_png and uploaded_csv:
            st.success("All required files have been uploaded. You may proceed to submission.")
            st.session_state["files_uploaded"] = True
        else:
            st.error("Please upload all required files: HTML, PNG, and CSV.")

    # Section 4: Submit Assignment
    st.header("Step 4: Submit Your Assignment")
    if st.button("Submit Assignment"):
        if not st.session_state.get("files_uploaded", False):
            st.error("You must upload all required files before submitting.")
        else:
            try:
                # Save uploaded files temporarily
                with open("temp_student_map.html", "wb") as f:
                    f.write(uploaded_html.read())
                with open("temp_student_chart.png", "wb") as f:
                    f.write(uploaded_png.read())
                with open("temp_student_summary.csv", "wb") as f:
                    f.write(uploaded_csv.read())

                # Grade the assignment using grade2.py
                grade = grade_assignment(
                    code,
                    "temp_student_map.html",
                    "temp_student_chart.png",
                    "temp_student_summary.csv"
                )

                # Display the grade
                st.success(f"Your grade: {grade}/100")

                # Save grade to Google Sheets
                update_google_sheet(student_id, grade, "assignment_2")
                st.success("Your grade has been successfully saved.")

            except Exception as e:
                st.error("An error occurred during grading. Please check your submission.")
                st.text_area("Error Details", traceback.format_exc(), height=200)


if __name__ == "__main__":
    show()
