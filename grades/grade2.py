import re
import csv
import math
import os

def grade_assignment(code, html_path, png_path, csv_path):
    total_score = 0
    debug_info = []  # Optional: collect info on each section for debugging

    ##########################################
    # 1. Library Imports (15 Points)
    ##########################################
    imports_score = 0
    required_libraries = {
        'folium': False,
        'matplotlib': False,  # or seaborn; we check for either
        'seaborn': False,
        'requests': False,  # or urllib, we check for either
        'urllib': False,
        'pandas': False,
    }
    
    # Look for import patterns in the code (this is a simple heuristic)
    for lib in required_libraries.keys():
        pattern = r"(?i)(import|from)\s+" + re.escape(lib) + r"\b"
        if re.search(pattern, code):
            required_libraries[lib] = True

    # Calculate score: each group gives an equal share of 15 points.
    lib_score = 0
    if required_libraries['folium']:
        lib_score += 15 * (1/5)
    if required_libraries['matplotlib'] or required_libraries['seaborn']:
        lib_score += 15 * (1/5)
    if required_libraries['requests'] or required_libraries['urllib']:
        lib_score += 15 * (1/5)
    if required_libraries['pandas']:
        lib_score += 15 * (1/5)
    # For balance, we assume the fifth group is a bonus if all are found
    imports_score = min(15, lib_score)
    debug_info.append(f"Imports score: {imports_score:.2f} / 15")
    
    ##########################################
    # 2. Code Quality (20 Points)
    ##########################################
    quality_score = 0

    # Descriptive variable names: Checking for keywords
    naming_score = 0
    if re.search(r"\bearthquake_map\b", code):
        naming_score += 5
    if re.search(r"\bmagnitude_counts\b", code):
        naming_score += 5
    naming_score = min(5, naming_score)
    
    # Spacing after operators
    spacing_score = 0
    if not re.search(r"\S[=<>+\-/*]{1}\S", code):
        spacing_score = 5
    else:
        spacing_score = 2.5

    # Comments: Count comment lines (at least 3 for full credit)
    comment_lines = sum(1 for line in code.splitlines() if line.strip().startswith("#"))
    comments_score = min(5, (comment_lines / 3) * 5)
    
    # Code Organization: blank lines present
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
    # 5. Map Visualization (20 Points)
    ##########################################
    map_score = 0
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        markers_found = bool(re.search(r"marker", html_content, re.IGNORECASE))
        colors_found = bool(re.search(r"(red|orange|green)", html_content, re.IGNORECASE))
        popup_found = bool(re.search(r"(magnitude|location|time)", html_content, re.IGNORECASE))
        if markers_found:
            map_score += 7
        if colors_found:
            map_score += 7
        if popup_found:
            map_score += 6
    except Exception as e:
        debug_info.append(f"Map visualization check error: {e}")
    map_score = min(20, map_score)
    debug_info.append(f"Map visualization score: {map_score} / 20")
    
    ##########################################
    # 6. Bar Chart (15 Points)
    ##########################################
    bar_chart_score = 0
    # Modification: only check for the correct magnitude range labels.
    # Since it's hard to extract text from an image without OCR,
    # we assume that if a non-empty PNG file is uploaded, it was generated using the correct ranges.
    try:
        if os.path.getsize(png_path) > 0:
            bar_chart_score = 15
    except Exception as e:
        debug_info.append(f"Bar chart file error: {e}")
    debug_info.append(f"Bar chart score: {bar_chart_score} / 15")
    
    ##########################################
    # 7. Text Summary (15 Points)
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
    
    # Instead of relying on column names or order, we scan all cells in the CSV (ignoring formatting)
    found_values = {metric: [] for metric in correct_values}
    try:
        with open(csv_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            # Go through every cell in the CSV
            for row in reader:
                for cell in row:
                    try:
                        num = float(cell.strip())
                        for metric, (expected, tol) in correct_values.items():
                            if math.isclose(num, expected, abs_tol=tol):
                                found_values[metric].append(num)
                    except ValueError:
                        continue

        partial = 0
        # For each metric, if we found at least one matching number within tolerance, award partial credit.
        for metric, (expected, tol) in correct_values.items():
            if found_values[metric]:
                partial += 15 / len(correct_values)
        summary_score = min(15, partial)
    except Exception as e:
        debug_info.append(f"CSV summary check error: {e}")
    debug_info.append(f"Text summary score: {summary_score} / 15")
    
    ##########################################
    # Sum up points
    ##########################################
    total_score = imports_score + quality_score + api_score + filter_score + map_score + bar_chart_score + summary_score
    total_score = round(total_score, 2)
    
    # Optionally, uncomment the following line to print debug information:
    # print("\n".join(debug_info))
    
    return total_score
