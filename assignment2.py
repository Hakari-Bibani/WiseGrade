import streamlit as st
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

# Fetch earthquake data from the USGS API
def fetch_earthquake_data(start_time, end_time):
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&endtime={end_time}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

# Filter earthquakes with magnitude > 4.0
def filter_earthquakes(data):
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

# Create an interactive map
def create_earthquake_map(earthquakes):
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

# Create a bar chart
def create_bar_chart(earthquakes):
    bins = [4.0, 4.5, 5.0, float('inf')]
    labels = ['4.0-4.5', '4.5-5.0', '5.0+']
    earthquakes['magnitude_range'] = pd.cut(earthquakes['magnitude'], bins=bins, labels=labels, right=False)
    magnitude_counts = earthquakes['magnitude_range'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    magnitude_counts.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Earthquake Frequency by Magnitude Range')
    ax.set_xlabel('Magnitude Range')
    ax.set_ylabel('Frequency')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=0)
    return fig

# Generate a text summary
def generate_text_summary(earthquakes):
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

    return pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])

# Main function
def main():
    st.title("Earthquake Data Analysis")
    st.markdown("This app fetches earthquake data from the USGS API and provides visualizations and summaries.")

    start_time = st.text_input("Start Date (YYYY-MM-DD)", "2025-01-02")
    end_time = st.text_input("End Date (YYYY-MM-DD)", "2025-01-09")

    if st.button("Fetch and Analyze Data"):
        data = fetch_earthquake_data(start_time, end_time)
        if data:
            earthquakes = filter_earthquakes(data)

            st.subheader("Interactive Map")
            earthquake_map = create_earthquake_map(earthquakes)
            st_folium(earthquake_map, width=700, height=500)

            st.subheader("Magnitude Distribution")
            bar_chart = create_bar_chart(earthquakes)
            st.pyplot(bar_chart)

            st.subheader("Summary Statistics")
            summary_df = generate_text_summary(earthquakes)
            st.dataframe(summary_df)

if __name__ == "__main__":
    main()
