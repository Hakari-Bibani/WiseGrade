import filecmp
import pandas as pd
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import pytesseract

# Define file paths
uploaded_map = "uploaded_map.html"
uploaded_chart = "uploaded_chart.png"
uploaded_csv = "uploaded_summary.csv"
correct_map = "correct_map.html"
correct_chart = "correct_chart.png"
correct_csv = "correct_summary.csv"

# Compare files byte-by-byte
print("### File Comparison ###")
map_match = filecmp.cmp(uploaded_map, correct_map, shallow=False)
chart_match = filecmp.cmp(uploaded_chart, correct_chart, shallow=False)
csv_match = filecmp.cmp(uploaded_csv, correct_csv, shallow=False)

print(f"Map files match: {map_match}")
print(f"Chart files match: {chart_match}")
print(f"CSV files match: {csv_match}")

# Compare bar chart structure
print("\n### Bar Chart Comparison ###")
try:
    uploaded_image = np.array(Image.open(uploaded_chart).convert("L"))
    correct_image = np.array(Image.open(correct_chart).convert("L"))
    similarity_score = ssim(uploaded_image, correct_image)
    print(f"Bar chart SSIM score: {similarity_score}")

    # OCR validation
    uploaded_text = pytesseract.image_to_string(uploaded_chart)
    print("Detected labels in uploaded chart:", uploaded_text)
except Exception as e:
    print(f"Error during bar chart comparison: {e}")

# Compare CSV files
print("\n### CSV Comparison ###")
try:
    uploaded_summary = pd.read_csv(uploaded_csv)
    correct_summary = pd.read_csv(correct_csv)

    uploaded_values = uploaded_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()
    correct_values = correct_summary.select_dtypes(include=["float", "int"]).to_numpy().flatten()

    tolerance = 0.01
    for i, (u, c) in enumerate(zip(uploaded_values, correct_values)):
        if abs(u - c) > tolerance:
            print(f"Mismatch at index {i}: Uploaded {u}, Correct {c}")
except Exception as e:
    print(f"Error during CSV comparison: {e}")

# Compare markers in map files
print("\n### Map Marker Comparison ###")
try:
    with open(uploaded_map, "r") as f:
        uploaded_map_data = BeautifulSoup(f, "html.parser")
    with open(correct_map, "r") as f:
        correct_map_data = BeautifulSoup(f, "html.parser")

    uploaded_markers = len(uploaded_map_data.find_all("circlemarker"))
    correct_markers = len(correct_map_data.find_all("circlemarker"))
    print(f"Uploaded markers: {uploaded_markers}, Correct markers: {correct_markers}")
except Exception as e:
    print(f"Error during map marker comparison: {e}")
