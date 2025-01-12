import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Fetch earthquake data
url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-01-02&endtime=2025-01-09"
response = requests.get(url)
data = response.json()

# Filter earthquakes with magnitude > 4.0
earthquakes = []
for feature in data['features']:
    if feature['properties']['mag'] > 4.0:
        earthquakes.append({
            'time': pd.to_datetime(feature['properties']['time'], unit='ms'),
            'latitude': feature['geometry']['coordinates'][1],
            'longitude': feature['geometry']['coordinates'][0],
            'magnitude': feature['properties']['mag']
        })
earthquakes = pd.DataFrame(earthquakes)

# Create a map
earthquake_map = folium.Map(location=[0, 0], zoom_start=2)
marker_cluster = MarkerCluster().add_to(earthquake_map)
for _, row in earthquakes.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Magnitude: {row['magnitude']}",
        icon=folium.Icon(color='green' if row['magnitude'] < 5.0 else 'red')
    ).add_to(marker_cluster)
