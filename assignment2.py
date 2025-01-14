import requests
import folium
import pandas as pd
import matplotlib.pyplot as plt

# Fetch earthquake data
url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-01-02&endtime=2025-01-09"
response = requests.get(url)
data = response.json()

# Filter earthquakes with magnitude > 4.0
earthquakes = [feature for feature in data['features'] if feature['properties']['mag'] > 4.0]

# Create a map
m = folium.Map(location=[0, 0], zoom_start=2)

# Add markers to the map
for eq in earthquakes:
    lat = eq['geometry']['coordinates'][1]
    lon = eq['geometry']['coordinates'][0]
    mag = eq['properties']['mag']
    time = pd.to_datetime(eq['properties']['time'], unit='ms').strftime('%Y-%m-%d %H:%M:%S')
    color = 'green' if 4 <= mag < 5 else 'yellow' if 5 <= mag < 5.5 else 'red'
    folium.Marker(
        location=[lat, lon],
        popup=f"Magnitude: {mag}<br>Time: {time}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Generate bar chart
magnitudes = [eq['properties']['mag'] for eq in earthquakes]
ranges = ['4.0-4.5', '4.5-5.0', '5.0+']
counts = [
    len([m for m in magnitudes if 4.0 <= m < 4.5]),
    len([m for m in magnitudes if 4.5 <= m < 5.0]),
    len([m for m in magnitudes if m >= 5.0])
]
fig, ax = plt.subplots()
ax.bar(ranges, counts)
ax.set_title("Earthquake Frequency by Magnitude Range")

# Text summary
summary = pd.DataFrame({
    "Total Earthquakes": [len(earthquakes)],
    "Average Magnitude": [sum(magnitudes) / len(magnitudes)],
    "Max Magnitude": [max(magnitudes)],
    "Min Magnitude": [min(magnitudes)]
})

# Display outputs
print(summary)
m
fig
