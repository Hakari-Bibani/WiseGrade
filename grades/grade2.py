import re
import csv
import math

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
    # We'll ignore case differences and spaces, and search both `import foo` and `from foo import ...`
    for lib in required_libraries.keys():
        pattern = r"(?i)(import|from)\s+" + re.escape(lib) + r"\b"
        if re.search(pattern, code):
            required_libraries[lib] = True

    # Now calculate score:
    # For libraries with alternatives we only require at least one to be present:
    lib_score = 0
    # folium (15 points contribution will be split among all library imports)
    if required_libraries['folium']:
        lib_score += 15 * (1/5)  # each of 5 groups gets equal share
    # matplotlib or seaborn group
    if required_libraries['matplotlib'] or required_libraries['seaborn']:
        lib_score += 15 * (1/5)
    # requests or urllib group
    if required_libraries['requests'] or required_libraries['urllib']:
        lib_score += 15 * (1/5)
    # pandas
    if required_libraries['pandas']:
        lib_score += 15 * (1/5)
    # (Fifth point bonus if all three groups found? Adjusting to total out of 15)
    # Scale the score so that maximum is 15:
    imports_score = min(15, lib_score)
    debug_info.append(f"Imports score: {imports_score:.2f} / 15")
    
    ##########################################
    # 2. Code Quality (20 Points)
    ##########################################
    quality_score = 0

    # Check for descriptive variable names:
    # This heuristic searches for variables in the code with names like: earthquake_map, magnitude_counts, etc.
    naming_score = 0
    if re.search(r"\bearthquake_map\b", code):
        naming_score += 5
    if re.search(r"\bmagnitude_counts\b", code):
        naming_score += 5
    # We limit descriptive names score to 5 points total.
    naming_score = min(5, naming_score)
    
    # Spacing after operators: a simple check if there is at least one instance of operator without space (like "=" with no space)
    spacing_score = 0
    if not re.search(r"\S[=<>+-/*]{1}\S", code):
        spacing_score = 5
    else:
        # if there are some issues, award 2.5 points
        spacing_score = 2.5

    # Comments explaining major steps
    comments_score = 0
    # count number of comment lines (lines that start with #)
    comment_lines = sum(1 for line in code.splitlines() if line.strip().startswith("#"))
    if comment_lines >= 3:
        comments_score = 5
    else:
        comments_score = (comment_lines / 3) * 5

    # Code Organization: check that there are blank lines in the code (i.e., multiple consecutive lines)
    organization_score = 0
    if re.search(r"\n\s*\n", code):
        organization_score = 5

    quality_score = naming_score + spacing_score + comments_score + organization_score
    quality_score = min(20, quality_score)
    debug_info.append(f"Quality score: {quality_score:.2f} / 20")
    
    ##########################################
    # 3. Fetching Data from the API (5 Points)
    ##########################################
    api_score = 0
    # Check if the code includes a URL with a query parameter for date range.
    # This is a heuristic: we search for something like "api" and "date" in the same line.
    if re.search(r"(https?://\S+api\S+\?[^'\"]*date)", code, re.IGNORECASE):
        api_score = 5
    debug_info.append(f"API score: {api_score} / 5")
    
    ##########################################
    # 4. Filtering Earthquakes (10 Points)
    ##########################################
    filter_score = 0
    # Check for filtering condition using magnitude ("> 4.0")
    if re.search(r"magnitude\s*[><=]+\s*4\.0", code):
        filter_score += 5
    # Check for extraction of latitude, longitude, magnitude, and time (a heuristic search)
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
    # We can check the uploaded HTML file for key elements that indicate the presence of markers and popups.
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        # Heuristics: check that the HTML contains the word "Marker" or "marker" and key data strings
        markers_found = bool(re.search(r"marker", html_content, re.IGNORECASE))
        colors_found = bool(re.search(r"(red|orange|green)", html_content, re.IGNORECASE))
        popup_found = bool(re.search(r"(magnitude|location|time)", html_content, re.IGNORECASE))
        if markers_found:
            map_score += 7  # out of 20
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
    # For the PNG file, we cannot easily inspect its content automatically without image processing.
    # Instead, we might require that the file exists and has a non-zero size.
    try:
        import os
        if os.path.getsize(png_path) > 0:
            bar_chart_score = 15
    except Exception as e:
        debug_info.append(f"Bar chart file error: {e}")
    debug_info.append(f"Bar chart score: {bar_chart_score} / 15")
    
    ##########################################
    # 7. Text Summary (15 Points)
    ##########################################
    summary_score = 0
    # The CSV file should include the rows with the correct metric values within tolerances.
    correct_values = {
        "Total Earthquakes (>4.0)": (218.0, 1),
        "Average Magnitude": (4.63, 0.1),
        "Maximum Magnitude": (7.1, 0.1),
        "Minimum Magnitude": (4.1, 0.1),
        "4.0-4.5": (75.0, 1),
        "4.5-5.0": (106.0, 1),
        "5.0+": (37.0, 1)
    }
    try:
        found_metrics = {}
        with open(csv_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    key = row[0].strip()
                    try:
                        val = float(row[1].strip())
                        found_metrics[key] = val
                    except:
                        continue

        # Now check each metric
        partial = 0
        for metric, (expected, tol) in correct_values.items():
            if metric in found_metrics:
                if math.isclose(found_metrics[metric], expected, abs_tol=tol):
                    partial += 15/len(correct_values)
        summary_score = min(15, partial)
    except Exception as e:
        debug_info.append(f"CSV summary check error: {e}")
    debug_info.append(f"Text summary score: {summary_score} / 15")
    
    ##########################################
    # Sum up points
    ##########################################
    total_score = imports_score + quality_score + api_score + filter_score + map_score + bar_chart_score + summary_score
    total_score = round(total_score, 2)
    
    # Optionally, you could print or log the debug_info to see how the grading went
    # For example: print("\n".join(debug_info))
    
    return total_score
