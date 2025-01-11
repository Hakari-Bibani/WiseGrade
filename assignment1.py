import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import hashlib
import re
import folium
from geopy.distance import geodesic
from streamlit_folium import folium_static

# Load Google Sheets API credentials securely
def load_google_sheets_api():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_creds"], scope)
    client = gspread.authorize(creds)
    return client

# Generate a unique Student ID
def generate_student_id(full_name, email):
    # Combine name and email, hash it, and take the first 4 digits + a letter
    combined = f"{full_name}{email}"
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    numbers = re.sub(r"[^0-9]", "", hashed)[:4]  # Extract first 4 digits
    letter = chr(ord('A') + int(numbers) % 26)  # Generate a letter
    return f"{numbers}{letter}"

# Save data to Google Sheets
def save_to_google_sheets(data):
    client = load_google_sheets_api()
    sheet = client.open("WG").sheet1
    df = pd.DataFrame(sheet.get_all_records())

    # Check if the email already exists
    if data["email"] in df["email"].values:
        # Update existing record
        index = df.index[df["email"] == data["email"]].tolist()[0]
        for key, value in data.items():
            sheet.update_cell(index + 2, df.columns.get_loc(key) + 1, value)
    else:
        # Append new record
        sheet.append_row(list(data.values()))

# Show the map using folium
def show(code):
    """
    Execute the student's code and display the map.
    """
    try:
        # Execute the code in a safe environment
        exec_globals = {"folium": folium, "geodesic": geodesic}
        exec_locals = {}
        exec(code, exec_globals, exec_locals)

        # Check if the map variable exists in the executed code
        if "mymap" in exec_locals:
            folium_static(exec_locals["mymap"])  # Display the map
        else:
            st.error("The code did not generate a map. Ensure the map variable is named 'mymap'.")
    except Exception as e:
        st.error(f"Error executing code: {e}")

# Streamlit UI
def main():
    st.title("Assignment Submission Portal")

    # Input fields
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID", value="", disabled=True)

    # Generate Student ID
    if full_name and email:
        student_id = generate_student_id(full_name, email)
        st.session_state.student_id = student_id

    # Tabbed interface
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.header("Assignment 1 Details")
        st.write("Plot three geographical coordinates on a map and calculate distances.")
        st.write("**Requirements:**")
        st.write("- Use `folium` for mapping.")
        st.write("- Use `geopy` for distance calculations.")
        st.write("- Submit your code below.")

        # Code input
        code = st.text_area("Paste your Python code here:", height=300)

        # Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Run"):
                if code:
                    show(code)  # Display the map using the 'show' method
                else:
                    st.warning("Please paste your code before running.")

        with col2:
            if st.button("Submit"):
                if full_name and email and student_id and code:
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
                        "total": 0,
                    }
                    save_to_google_sheets(data)
                    st.success("Assignment submitted successfully!")
                else:
                    st.warning("Please fill all fields before submitting.")

    with tab2:
        st.header("Grading Details")
        st.write("Your grades will be displayed here after submission.")

if __name__ == "__main__":
    main()
