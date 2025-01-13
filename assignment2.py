import streamlit as st
import pandas as pd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime
from io import StringIO
from streamlit_folium import st_folium
from utils.style1 import set_page_style
from Record.google_sheet import fetch_student_record, update_google_sheet

def fetch_earthquake_data(start_date, end_date):
    """Fetch earthquake data from the USGS Earthquake API."""
    url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

def process_earthquake_data(data):
    """Process raw earthquake data and filter by magnitude."""
    features = data.get("features", [])
    processed_data = []
    for feature in features:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        magnitude = props.get("mag", 0)
        if magnitude > 4.0:
            processed_data.append({
                "Latitude": coords[1],
                "Longitude": coords[0],
                "Magnitude": magnitude,
                "Location": props.get("place", "Unknown"),
                "Time": datetime.utcfromtimestamp(props.get("time") / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            })
    return pd.DataFrame(processed_data)

def create_map(data):
    """Create a Folium map with earthquake markers."""
    earthquake_map = folium.Map(location=[36.0, -100.0], zoom_start=2)
    for _, row in data.iterrows():
        color = "green" if row["Magnitude"] <= 5 else "yellow" if row["Magnitude"] <= 5.5 else "red"
        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            popup=f"Magnitude: {row['Magnitude']}\nLocation: {row['Location']}\nTime: {row['Time']}",
            icon=folium.Icon(color=color),
        ).add_to(earthquake_map)
    return earthquake_map

def generate_bar_chart(data):
    """Generate a bar chart for earthquake frequency by magnitude range."""
    ranges = {"4.0-4.5": 0, "4.5-5.0": 0, ">5.0": 0}
    for mag in data["Magnitude"]:
        if 4.0 <= mag < 4.5:
            ranges["4.0-4.5"] += 1
        elif 4.5 <= mag <= 5.0:
            ranges["4.5-5.0"] += 1
        else:
            ranges[">5.0"] += 1
    df = pd.DataFrame(list(ranges.items()), columns=["Magnitude Range", "Frequency"])
    
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="Magnitude Range", y="Frequency", ax=ax)
    ax.set_title("Earthquake Frequency by Magnitude Range")
    ax.set_xlabel("Magnitude Range")
    ax.set_ylabel("Frequency")
    return fig, df

def show():
    # Apply the custom page style
    set_page_style()

    st.title("Assignment 2: Real-Time Earthquake Data Visualization and Analysis")

    # Student ID Input
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Student ID")
    
    # Validate Student ID
    if st.button("Validate Student ID"):
        student_record = fetch_student_record(student_id)
        if student_record:
            if student_record.get("assignment_2_submitted"):
                st.error("You have already submitted Assignment 2.")
                st.stop()
            st.success("Student ID validated. Proceed to the next steps.")
        else:
            st.error("Invalid Student ID. Please ensure you have submitted Assignment 1.")

    # Fetch Earthquake Data
    st.header("Step 2: Fetch and Process Earthquake Data")
    start_date = "2025-01-02"
    end_date = "2025-01-09"

    if st.button("Fetch Data"):
        raw_data = fetch_earthquake_data(start_date, end_date)
        if raw_data:
            earthquake_data = process_earthquake_data(raw_data)
            if earthquake_data.empty:
                st.warning("No earthquakes with magnitude > 4.0 found in the specified range.")
                st.stop()
            else:
                st.success("Earthquake data fetched and processed successfully.")

    # Visualizations
    st.header("Step 3: Visualize the Data")
    if 'earthquake_data' in locals() or 'earthquake_data' in globals():
        st.markdown("### Interactive Map")
        map_object = create_map(earthquake_data)
        st_folium(map_object, width=700, height=500)

        st.markdown("### Bar Chart")
        bar_chart, bar_chart_df = generate_bar_chart(earthquake_data)
        st.pyplot(bar_chart)

        st.markdown("### Summary Table")
        st.write(bar_chart_df)

        total_earthquakes = len(earthquake_data)
        avg_magnitude = earthquake_data["Magnitude"].mean()
        max_magnitude = earthquake_data["Magnitude"].max()
        min_magnitude = earthquake_data["Magnitude"].min()

        summary = pd.DataFrame({
            "Metric": ["Total Earthquakes", "Average Magnitude", "Maximum Magnitude", "Minimum Magnitude"],
            "Value": [total_earthquakes, avg_magnitude, max_magnitude, min_magnitude],
        })
        summary["Value"] = summary["Value"].apply(lambda x: f"{x:.2f}")
        st.markdown("### Summary Statistics")
        st.write(summary)

    # Submission
    st.header("Step 4: Submit Assignment")
    if st.button("Submit Assignment"):
        if 'earthquake_data' not in locals() and 'earthquake_data' not in globals():
            st.error("Please fetch and process earthquake data before submitting.")
        elif student_id:
            update_google_sheet(student_id, "assignment_2_submitted", True)
            st.success("Assignment 2 submitted successfully!")
        else:
            st.error("Invalid Student ID. Please validate it first.")
