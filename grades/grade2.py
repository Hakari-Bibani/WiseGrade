import re
import csv
import math
import os
from PIL import Image
import pytesseract

# Configure pytesseract (update the path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def grade_assignment(code, html_path, png_path, csv_path):
    total_score = 0
    debug_info = []

    ##########################################
    # 1. Library Imports (15 Points)
    ##########################################
    imports_score = 0
    required_libraries = {
        'folium': False,
        'matplotlib': False,  # or seaborn; we check for either
        'seaborn': False,
        'requests': False,     # or urllib
        'urllib': False,
        'pandas': False,
    }
    
    for lib in required_libraries.keys():
        pattern = r"(?i)(import|from)\s+" + re.escape(lib) + r"\b"
        if re.search(pattern, code):
            required_libraries[lib] = True

    lib_score = 0
    if required_libraries['folium']:
        lib_score += 15 * (1/5)
    if required_libraries['matplotlib'] or required_libraries['seaborn']:
        lib_score += 15 * (1/5)
    if required_libraries['requests'] or required_libraries['urllib']:
        lib_score += 15 * (1/5)
    if required_libraries['pandas']:
        lib_score += 15 * (1/5)
    # Cap the imports score at 15
    imports_score = min(15, lib_score)
    debug_info.append(f"Imports score: {imports_score:.2f} / 15")
    
    ##########################################
    # 2. Code Quality (20 Points)
    ##########################################
    # Descriptive Variable Names (5 Points)
    naming_score = 0
    if re.search(r"\bearthquake_map\b", code):
        naming_score += 5
    if re.search(r"\bmagnitude_counts\b", code):
        naming_score += 5
    naming_score = min(5, naming_score)
    
    # Spacing After Operators (5 Points)
    spacing_score = 0
    if not re.search(r"\S[=<>+\-/*]{1}\S", code):
        spacing_score = 5
    else:
        spacing_score = 2.5

    # Comments (5 Points)
    comment_lines = sum(1 for line in code.splitlines() if line.strip().startswith("#"))
    comments_score = min(5, (comment_lines / 3) * 5)
    
    # Code Organization (5 Points)
    organization_score = 5 if re.search(r"\n\s*\n", code) else 0

    quality_score = naming_score + spacing_score + comments_score + organization_score
    quality_score = min(20, quality_score)
    debug_info.append(f"Quality score: {quality_score:.2f} / 20")
    
    ##########################################
    # 3. Fetching Data from the API (5 Points)
    ##########################################
    api_score = 0
    if re.search(r"(https?://\S+api\S+\?[^'\"]*date)", code, re.IGNORECASE):
        api_score = 5
    debug_info.append(f"API score: {api_score} / 5")
    
    ##########################################
    # 4. Filtering Earthquakes (10 Points)
    ##########################################
    filter_score = 0
    if re.search(r"magnitude\s*[><=]+\s*4\.0", code):
        filter_score += 5
    extraction_hits = 0
    for field in ["latitude", "longitude", "magnitude", "time"]:
        if re.search(field, code, re.IGNORECASE):
            extraction_hits += 1
    if extraction_hits >= 4:
        filter_score += 5
    debug_info.append(f"Filter score: {filter_score} / 10")
    
    ##########################################
    # 5. Map Visualization (25 Points)
    ##########################################
    map_score = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # (a) Check for any type of marker — 10 points
        if re.search(r"L\.(Circle)?Marker\(\[.*?\]\)", html_content, re.IGNORECASE):
            map_score += 10
        
        # (b) Check for color keywords for markers (green, red, yellow) — 10 points
        colors_found = 0
        for color in ["green", "red", "yellow"]:
            if re.search(fr"color\s*:\s*['\"]{color}['\"]", html_content, re.IGNORECASE):
                colors_found += 1
        if colors_found == 3:
            map_score += 10
        else:
            map_score += 10 * (colors_found / 3)
        
        # (c) Check for popups that include “magnitude”, “location”, “time” — 5 points
        popup_hits = 0
        for keyword in ["magnitude", "location", "time"]:
            if re.search(fr"\.bindPopup\(\s*['\"].*?{keyword}.*?['\"]\)", html_content, re.IGNORECASE):
                popup_hits += 1
        if popup_hits == 3:
            map_score += 5
        else:
            map_score += 5 * (popup_hits / 3)
    except Exception as e:
        debug_info.append(f"Map visualization check error: {e}")
    map_score = min(25, map_score)
    debug_info.append(f"Map visualization score: {map_score} / 25")
    
    ##########################################
    # 6. Bar Chart (PNG) (5 Points)
    ##########################################
    bar_chart_score = 0
    # Expected labels for the bar chart:
    expected_labels = ["4.0-4.5", "4.5-5.0", ">5.0"]
    
    if pytesseract is None:
        # Fallback: if OCR is not available, only check that file exists.
        try:
            if os.path.getsize(png_path) > 0:
                # Not ideal: this gives full points even if label check cannot be done.
                bar_chart_score = 5
        except Exception as e:
            debug_info.append(f"Bar chart file error: {e}")
    else:
        try:
            img = Image.open(png_path)
            ocr_text = pytesseract.image_to_string(img)
            # Debug: Uncomment the next line to print OCR text if needed
            # print("OCR Text:", ocr_text)
            for label in expected_labels:
                if label in ocr_text:
                    bar_chart_score += 5 / 3  # 5 points split across 3 labels
        except Exception as e:
            debug_info.append(f"Bar chart OCR error: {e}")
    bar_chart_score = min(5, bar_chart_score)
    debug_info.append(f"Bar chart score: {bar_chart_score} / 5")
    
    ##########################################
    # 7. Text Summary (CSV) (20 Points)
    ##########################################
    summary_score = 0
    # Expected values and tolerances:
    correct_values = {
        "Total Earthquakes (>4.0)": (218.0, 1),
        "Average Magnitude": (4.63, 0.1),
        "Maximum Magnitude": (7.1, 0.1),
        "Minimum Magnitude": (4.1, 0.1),
        "4.0-4.5": (75.0, 1),
        "4.5-5.0": (106.0, 1),
        "5.0+": (37.0, 1)
    }
    
    # We ignore header and formatting differences: check every cell.
    found_values = {metric: False for metric in correct_values}
    try:
        with open(csv_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for cell in row:
                    try:
                        num = float(cell.strip())
                        for metric, (expected, tol) in correct_values.items():
                            if not found_values[metric] and math.isclose(num, expected, abs_tol=tol):
                                found_values[metric] = True
                    except ValueError:
                        continue
        partial = 0
        total_metrics = len(correct_values)
        for metric in correct_values:
            if found_values[metric]:
                partial += 20 / total_metrics  # 20 points split across 7 metrics
        summary_score = min(20, partial)
    except Exception as e:
        debug_info.append(f"CSV summary check error: {e}")
    debug_info.append(f"Text summary score: {summary_score} / 20")
    
    ##########################################
    # Total Score
    ##########################################
    total_score = imports_score + quality_score + api_score + filter_score + map_score + bar_chart_score + summary_score
    total_score = round(total_score, 2)
    
    # Uncomment to print detailed debug info if needed:
    # print("\n".join(debug_info))
    
    return total_score, debug_info
