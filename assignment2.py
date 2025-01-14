import streamlit as st
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

# Fetch earthquake data from the USGS API
def fetch_earthquake_data(start_time, end_time):
    """
    Fetches earthquake data from the USGS API for the specified date range.
    """
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&endtime={end_time}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# Filter earthquakes with magnitude > 4.0
def filter_earthquakes(data):
    """
    Filters earthquakes with magnitude greater than 4.0.
    """
    features = data['features']
    earthquakes = []
    for feature in features:
        properties = feature['properties']
        geometry = feature['geometry']
        magnitude = properties['mag']
        if magnitude > 4.0:
            earthquake = {
                'time': pd.to_datetime(properties['time'], unit='ms'),
                'latitude': geometry['coordinates'][1],
                'longitude': geometry['coordinates'][0],
                'magnitude': magnitude
            }
            earthquakes.append(earthquake)
    return pd.DataFrame(earthquakes)

# Generate an interactive map with color-coded markers
def create_earthquake_map(earthquakes):
    """
    Creates an interactive map with markers for each earthquake.
    Markers are color-coded based on magnitude:
    - Green: 4.0-5.0
    - Yellow: 5.0-5.5
    - Red: 5.5+
    """
    earthquake_map = folium.Map(location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(earthquake_map)

    for _, row in earthquakes.iterrows():
        magnitude = row['magnitude']
        if 4.0 <= magnitude < 5.0:
            color = 'green'
        elif 5.0 <= magnitude < 5.5:
            color = 'yellow'
        else:
            color = 'red'

        popup = folium.Popup(
            f"Magnitude: {magnitude}<br>"
            f"Location: ({row['latitude']}, {row['longitude']})<br>"
            f"Time: {row['time']}"
        )
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)

    return earthquake_map

# Generate a bar chart for earthquake frequency by magnitude range
def create_bar_chart(earthquakes):
    """
    Creates a bar chart showing earthquake frequency in the following magnitude ranges:
    - 4.0-4.5
    - 4.5-5.0
    - 5.0+
    """
    bins = [4.0, 4.5, 5.0, float('inf')]
    labels = ['4.0-4.5', '4.5-5.0', '5.0+']
    earthquakes['magnitude_range'] = pd.cut(earthquakes['magnitude'], bins=bins, labels=labels, right=False)
    magnitude_counts = earthquakes['magnitude_range'].value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    magnitude_counts.plot(kind='bar', color='skyblue')
    plt.title('Earthquake Frequency by Magnitude Range')
    plt.xlabel('Magnitude Range')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)
    return plt

# Generate a text summary of the earthquake data
def generate_text_summary(earthquakes):
    """
    Generates a text summary of the earthquake data, including:
    - Total number of earthquakes with magnitude > 4.0
    - Average, maximum, and minimum magnitudes
    - Number of earthquakes in each magnitude range
    """
    total_earthquakes = len(earthquakes)
    avg_magnitude = earthquakes['magnitude'].mean()
    max_magnitude = earthquakes['magnitude'].max()
    min_magnitude = earthquakes['magnitude'].min()

    bins = [4.0, 4.5, 5.0, float('inf')]
    labels = ['4.0-4.5', '4.5-5.0', '5.0+']
    earthquakes['magnitude_range'] = pd.cut(earthquakes['magnitude'], bins=bins, labels=labels, right=False)
    magnitude_counts = earthquakes['magnitude_range'].value_counts().sort_index()

    summary = {
        'Total Earthquakes': total_earthquakes,
        'Average Magnitude': round(avg_magnitude, 2),
        'Maximum Magnitude': round(max_magnitude, 2),
        'Minimum Magnitude': round(min_magnitude, 2),
        'Earthquakes in 4.0-4.5': magnitude_counts.get('4.0-4.5', 0),
        'Earthquakes in 4.5-5.0': magnitude_counts.get('4.5-5.0', 0),
        'Earthquakes in 5.0+': magnitude_counts.get('5.0+', 0)
    }

    # Convert summary to DataFrame
    summary_df = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])
    return summary_df

# Streamlit app
def main():
    st.title("Earthquake Data Analysis")

    # Define date range
    start_time = "2025-01-02"
    end_time = "2025-01-09"

    # Fetch and filter earthquake data
    st.write("Fetching earthquake data...")
    data = fetch_earthquake_data(start_time, end_time)
    earthquakes = filter_earthquakes(data)
    st.write(f"Found {len(earthquakes)} earthquakes with magnitude > 4.0.")

    # Create and display the earthquake map
    st.write("Generating earthquake map...")
    earthquake_map = create_earthquake_map(earthquakes)
    st_folium(earthquake_map, width=700, height=500)

    # Create and display the bar chart
    st.write("Generating bar chart...")
    bar_chart = create_bar_chart(earthquakes)
    st.pyplot(bar_chart)

    # Generate and display the text summary
    st.write("Generating text summary...")
    summary_df = generate_text_summary(earthquakes)
    st.dataframe(summary_df)

# Run the Streamlit app
if __name__ == "__main__":
    main()
