import streamlit as st
import random
import string
from style1 import apply_custom_styles
from grade1 import calculate_grade
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["GOOGLE_SHEET_KEY"], scope)
gc = gspread.authorize(credentials)
sheet = gc.open("WG").sheet1  # Open Google Sheet

def generate_student_id(full_name, email):
    unique_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{unique_part}-{email[:1].upper()}"

def app():
    st.title("Assignment 1 Submission")
    apply_custom_styles()

    # Tabs for UI
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    # Tab 1: Assignment Details
    with tab1:
        st.subheader("Assignment Details")
        st.write("Objective: Write a Python script to plot three coordinates on a map and calculate distances.")
        if st.button("Read More"):
            st.write("""
                - Use geopy and folium libraries.
                - Expected outputs: Map visualization and CSV summary.
            """)

        # User Inputs
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        if full_name and email:
            student_id = generate_student_id(full_name, email)
            st.text_input("Student ID (Auto-generated)", student_id, disabled=True)

    # Tab 2: Code Submission
    with tab2:
        st.subheader("Submit Your Code")
        code_input = st.text_area("Paste your code here:")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Run"):
                try:
                    exec(code_input)  # Unsafe in production; consider alternatives
                    st.success("Code executed successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

        with col2:
            if st.button("Submit"):
                grade = calculate_grade(code_input)
                st.success(f"Grade: {grade}/100")

                # Save or update submission in Google Sheet
                existing_data = sheet.get_all_records()
                found = False
                for i, row in enumerate(existing_data, start=2):  # Skip header
                    if row["email"] == email:
                        found = True
                        sheet.update(f"D{i}", grade)  # Update assignment_1
                        st.info("Submission updated.")
                        break
                if not found:
                    # Insert new row
                    sheet.append_row([full_name, email, student_id, grade, "", "", "", "", "", "", ""])
                    st.info("Submission saved.")

