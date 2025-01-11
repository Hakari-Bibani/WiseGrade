import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import hashlib
import re

# Load Google Sheets API credentials from Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_credentials"], scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("WG").sheet1

# Function to generate a unique Student ID
def generate_student_id(full_name, email):
    # Create a hash of the full name and email
    combined = f"{full_name}{email}"
    hash_object = hashlib.sha256(combined.encode())
    hex_dig = hash_object.hexdigest()
    # Extract the first 4 digits and a letter
    student_id = hex_dig[:4] + chr(ord('A') + int(hex_dig[4], 16) % 26)
    return student_id

# Function to save data to Google Sheets
def save_to_google_sheets(data):
    # Check if the email already exists in the sheet
    records = sheet.get_all_records()
    email_exists = any(record["email"] == data["email"] for record in records)
    
    if email_exists:
        # Update the existing record
        for i, record in enumerate(records):
            if record["email"] == data["email"]:
                row_index = i + 2  # +2 because of header and 0-based index
                sheet.update(f"A{row_index}:L{row_index}", [list(data.values())])
                break
    else:
        # Append a new record
        sheet.append_row(list(data.values()))

# Streamlit UI
st.title("Assignment Submission Portal")

# Input fields
full_name = st.text_input("Full Name")
email = st.text_input("Email")

# Generate Student ID
if full_name and email:
    student_id = generate_student_id(full_name, email)
    st.text_input("Student ID", value=student_id, disabled=True)
else:
    student_id = None

# Tabbed interface
tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

with tab1:
    st.header("Assignment 1 Details")
    st.write("Plot three geographical coordinates on a map and calculate distances.")
    st.write("**Requirements:**")
    st.write("- Use `folium` for mapping.")
    st.write("- Use `geopy` for distance calculations.")
    st.write("- Submit your code below.")

    # Code input cell
    code = st.text_area("Paste your Python code here:", height=300)

    # Buttons for running and submitting code
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run Code"):
            if code:
                try:
                    # Execute the code and capture output
                    exec(code)
                    st.success("Code executed successfully!")
                except Exception as e:
                    st.error(f"Error executing code: {e}")
            else:
                st.warning("Please paste your code before running.")

    with col2:
        if st.button("Submit Assignment"):
            if full_name and email and student_id and code:
                # Save data to Google Sheets
                data = {
                    "full_name": full_name,
                    "email": email,
                    "student_ID": student_id,
                    "assignment_1": code,
                    "assignment_2": "",
                    "assignment_3": "",
                    "assignment_4": "",
                    "quiz_1": "",
                    "quiz_2": "",
                    "quiz_3": "",
                    "quiz_4": "",
                    "total": 0
                }
                save_to_google_sheets(data)
                st.success("Assignment submitted successfully!")
            else:
                st.warning("Please fill all fields before submitting.")

with tab2:
    st.header("Grading Details")
    st.write("Your grades will be displayed here after submission.")
