import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
from style1 import apply_style
from grade1 import calculate_grade

# Apply custom styles
apply_style()

# Load Google Sheets API credentials
@st.cache_data
def load_google_sheets_credentials():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return gspread.authorize(credentials)

# Initialize Google Sheets client
client = load_google_sheets_credentials()
sheet = client.open("WG").sheet1

# Function to generate Student ID
def generate_student_id(full_name, email):
    import hashlib
    hash_input = f"{full_name}{email}".encode("utf-8")
    hash_output = hashlib.md5(hash_input).hexdigest()
    student_id = f"{hash_output[:4]}{hash_output[4].upper()}"
    return student_id

# Function to save data to Google Sheets
def save_to_google_sheets(data):
    sheet.append_row(data)

# Function to update data in Google Sheets
def update_google_sheets(email, data):
    records = sheet.get_all_records()
    for i, row in enumerate(records):
        if row["email"] == email:
            sheet.update_cell(i + 2, 4, data["assignment_1"])  # Update assignment_1 column
            break

# Streamlit UI
st.title("Assignment Submission Portal")

# Input fields
full_name = st.text_input("Full Name")
email = st.text_input("Email")

# Generate Student ID
if full_name and email:
    student_id = generate_student_id(full_name, email)
    st.write(f"**Student ID:** {student_id}")
else:
    student_id = None

# Tabbed interface
tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

with tab1:
    st.header("Assignment Details")
    st.write("""
    **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**

    **Objective:**
    In this assignment, you will write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers. This will help you practice working with geospatial data and Python libraries for mapping and calculations.
    """)

with tab2:
    st.header("Grading Details")
    st.write("""
    **a. Library Imports (5 points)**
    - **Description:** Checks if the required libraries (`folium`, `geopy`, `geodesic`) are imported.
    - **Points Allocation:**
      - 1.67 points per correct import (total of 3 libraries).
    - **How Points Are Awarded:**
      - If all three libraries are imported: 5 points.
    """)

# Code submission
st.header("Code Submission")
code = st.text_area("Paste your Python code here:", height=300)

# Buttons for Run and Submit
col1, col2 = st.columns(2)
with col1:
    if st.button("Run"):
        if code:
            try:
                exec(code)
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {e}")
        else:
            st.warning("Please paste your code before running.")

with col2:
    if st.button("Submit"):
        if full_name and email and student_id and code:
            # Calculate grade
            grade = calculate_grade(code)

            # Prepare data for Google Sheets
            data = [full_name, email, student_id, grade, "", "", "", "", "", "", "", ""]

            # Check if the student has already submitted assignment_1
            records = sheet.get_all_records()
            existing_entry = next((row for row in records if row["email"] == email), None)

            if existing_entry:
                if existing_entry["assignment_2"]:  # If assignment_2 is submitted, prevent resubmission
                    st.error("You cannot resubmit Assignment 1 after submitting Assignment 2.")
                else:
                    update_google_sheets(email, {"assignment_1": grade})
                    st.success("Assignment 1 updated successfully!")
            else:
                save_to_google_sheets(data)
                st.success("Assignment 1 submitted successfully!")
        else:
            st.warning("Please fill in all fields before submitting.")
