import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import folium
from streamlit_folium import folium_static
from utils.style1 import apply_style
from grades.grade1 import calculate_grade
import google_sheet  # Custom module to interact with Google Sheets API

# Apply custom styles
apply_style()

# Function to generate Student ID
def generate_student_id(full_name, email):
    import hashlib
    unique_string = f"{full_name}{email}"
    hash_object = hashlib.md5(unique_string.encode())
    hash_hex = hash_object.hexdigest()
    student_id = hash_hex[:4].upper() + "A"  # Example: 4 numbers + 1 alphabet
    return student_id

# Function to calculate distances between coordinates
def calculate_distances(point1, point2, point3):
    distance_1_2 = geodesic(point1, point2).kilometers
    distance_2_3 = geodesic(point2, point3).kilometers
    distance_1_3 = geodesic(point1, point3).kilometers
    return distance_1_2, distance_2_3, distance_1_3

# Function to plot coordinates on a map
def plot_map(point1, point2, point3):
    map_center = point1
    mymap = folium.Map(location=map_center, zoom_start=8)
    folium.Marker(location=point1, popup="Point 1").add_to(mymap)
    folium.Marker(location=point2, popup="Point 2").add_to(mymap)
    folium.Marker(location=point3, popup="Point 3").add_to(mymap)
    folium.PolyLine(locations=[point1, point2, point3], color="blue").add_to(mymap)
    return mymap

# Main function for the assignment
def assignment1():
    st.title("Assignment 1: Mapping Coordinates and Calculating Distances")

    # Input fields for Full Name and Email
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")

    # Generate Student ID
    if full_name and email:
        student_id = generate_student_id(full_name, email)
        st.write(f"Your Student ID: **{student_id}**")
    else:
        student_id = None

    # Tabbed interface for Assignment and Grading Details
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.write("""
        **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**

        **Objective:**
        In this assignment, you will write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers. This will help you practice working with geospatial data and Python libraries for mapping and calculations.
        """)

    with tab2:
        st.write("""
        **Grading Details:**

        **a. Library Imports (5 points)**
        - Description: Checks if the required libraries (`folium`, `geopy`, `geodesic`) are imported.
        - Points Allocation:
          - 1.67 points per correct import (total of 3 libraries).
        - How Points Are Awarded:
          - If all three libraries are imported: 5 points.
        """)

    # Code input cell
    st.subheader("Code Submission")
    user_code = st.text_area("Paste your Python code here:", height=300)

    # Buttons for Run and Submit
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run"):
            try:
                # Execute user code
                exec(user_code)
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {e}")

    with col2:
        if st.button("Submit"):
            if not student_id:
                st.error("Please fill in Full Name and Email to generate Student ID.")
            else:
                # Calculate grade
                grade = calculate_grade(user_code)
                st.write(f"Your Grade: **{grade}/100**")

                # Save data to Google Sheet
                data = {
                    "full_name": full_name,
                    "email": email,
                    "student_ID": student_id,
                    "assignment_1": grade,
                }
                google_sheet.save_to_sheet(data)  # Save to Google Sheet
                st.success("Submission saved successfully!")

# Run the assignment
if __name__ == "__main__":
    assignment1()
