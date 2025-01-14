import requests
import folium
import pandas as pd
import matplotlib.pyplot as plt

# Fetch earthquake data
url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-01-02&endtime=2025-01-09"
response = requests.get(url)
data = response.json()

# Filter earthquakes with magnitude > 4.0
earthquakes = [
    {
        "latitude": feature["geometry"]["coordinates"][1],
        "longitude": feature["geometry"]["coordinates"][0],
        "magnitude": feature["properties"]["mag"],
        "time": pd.to_datetime(feature["properties"]["time"], unit="ms")
    }
    for feature in data["features"] if feature["properties"]["mag"] > 4.0
]

# Create a map
m = folium.Map(location=[0, 0], zoom_start=2)
for eq in earthquakes:
    color = "green" if 4 <= eq["magnitude"] < 5 else "yellow" if 5 <= eq["magnitude"] < 5.5 else "red"
    folium.Marker(
        location=[eq["latitude"], eq["longitude"]],
        popup=f"Magnitude: {eq['magnitude']}\nTime: {eq['time']}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Generate a bar chart
magnitude_ranges = ["4.0-4.5", "4.5-5.0", "5.0+"]
counts = [
    sum(4 <= eq["magnitude"] < 4.5 for eq in earthquakes),
    sum(4.5 <= eq["magnitude"] < 5.0 for eq in earthquakes),
    sum(eq["magnitude"] >= 5.0 for eq in earthquakes)
]
fig, ax = plt.subplots()
ax.bar(magnitude_ranges, counts)
ax.set_title("Earthquake Frequency by Magnitude")
ax.set_xlabel("Magnitude Range")
ax.set_ylabel("Number of Earthquakes")

# Text summary
total_earthquakes = len(earthquakes)
avg_magnitude = sum(eq["magnitude"] for eq in earthquakes) / total_earthquakes
max_magnitude = max(eq["magnitude"] for eq in earthquakes)
min_magnitude = min(eq["magnitude"] for eq in earthquakes)
text_summary = f"""
Total Earthquakes: {total_earthquakes}
Average Magnitude: {avg_magnitude:.2f}
Maximum Magnitude: {max_magnitude:.2f}
Minimum Magnitude: {min_magnitude:.2f}
Number of Earthquakes by Magnitude Range:
- 4.0-4.5: {counts[0]}
- 4.5-5.0: {counts[1]}
- 5.0+: {counts[2]}
"""
