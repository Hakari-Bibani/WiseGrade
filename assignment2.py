# Import necessary libraries
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt

# Fetch earthquake data from the USGS API
def fetch_earthquake_data(start_time, end_time):
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&endtime={end_time}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

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

# Generate an interactive map with color-coded markers
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

# Main execution
# Define date range
start_time = "2025-01-02"
end_time = "2025-01-09"

# Fetch and filter earthquake data
data = fetch_earthquake_data(start_time, end_time)
earthquakes = filter_earthquakes(data)

# Create and save the map
earthquake_map = create_earthquake_map(earthquakes)
st.session_state.outputs["map"] = earthquake_map

# Create bar chart
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
plt.tight_layout()
st.session_state.outputs["chart"] = plt.gcf()

# Generate summary
summary = {
    'Total Earthquakes': len(earthquakes),
    'Average Magnitude': round(earthquakes['magnitude'].mean(), 2),
    'Maximum Magnitude': round(earthquakes['magnitude'].max(), 2),
    'Minimum Magnitude': round(earthquakes['magnitude'].min(), 2),
    'Earthquakes in 4.0-4.5': magnitude_counts.get('4.0-4.5', 0),
    'Earthquakes in 4.5-5.0': magnitude_counts.get('4.5-5.0', 0),
    'Earthquakes in 5.0+': magnitude_counts.get('5.0+', 0)
}

# Create and display summary DataFrame
summary_df = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])
st.session_state.outputs["summary"] = summary_df

# Print some information
print(f"Found {len(earthquakes)} earthquakes with magnitude > 4.0")
print(f"Average magnitude: {earthquakes['magnitude'].mean():.2f}")
