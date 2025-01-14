import pandas as pd
import re
import json

def grade_assignment(code):
    grade = 0

    # 1. Code Implementation (30 points)
    if "requests" in code or "urllib" in code:
        grade += 10
    if "folium" in code and "matplotlib" in code:
        grade += 10
    if "json" in code:
        grade += 10

    # 2. Visualization (40 points)
    if "folium.Map" in code:
        grade += 20
    if "Marker" in code and "popup" in code:
        grade += 10
    if "bar" in code or "plt.bar" in code:
        grade += 10

    # 3. Summary (30 points)
    if "Total number of earthquakes" in code:
        grade += 10
    if "average" in code and "maximum" in code and "minimum" in code:
        grade += 10
    if "csv" in code:
        grade += 10

    return grade
