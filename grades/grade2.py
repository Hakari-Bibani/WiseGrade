import re

def grade_assignment(code_input):
    """
    Grades the Assignment 2 code based on the specified rubric.
    Returns an integer score out of 100.
    
    NOTE: This grading function uses naive, text-based heuristics.
    It does not perform advanced parsing or execution checks. 
    Feel free to refine as needed.
    """
    # Total possible points as described in the rubric = 110
    # We will later scale to 100.
    
    total_score = 0
    
    # --- 1. Library Imports (10 Points) ---
    cat1_score = 0
    
    # Check presence of required libraries
    # Each found library => +2 points. Missing => no points for that item. 
    # We'll do a naive search:
    libraries_needed = {
        'folium': False,       # for map
        'matplotlib': False,   # or seaborn for bar chart
        'seaborn': False,      
        'requests': False,     # or urllib for API calls
        'urllib': False,
        'pandas': False
    }
    
    # We'll scan line by line for import statements
    lines = code_input.split('\n')
    imported_libraries = []
    for line in lines:
        line_stripped = line.strip()
        # capture something like "import X" or "from X import"
        # We'll do a basic parse
        if line_stripped.startswith("import ") or line_stripped.startswith("from "):
            imported_libraries.append(line_stripped)
    
    # Mark which libraries are found
    for lib in libraries_needed.keys():
        # We'll consider it found if code mentions "import <lib>" or "from <lib>" 
        if re.search(rf"(import|from)\s+{lib}\b", code_input):
            libraries_needed[lib] = True

    # We only need ONE of matplotlib or seaborn => If either is True, we consider the bar-chart library satisfied
    bar_chart_lib_found = libraries_needed['matplotlib'] or libraries_needed['seaborn']
    # We only need ONE of requests or urllib => If either is True, we consider the requests library satisfied
    requests_lib_found = libraries_needed['requests'] or libraries_needed['urllib']

    # Points for each successfully imported library
    #   folium => 2
    #   matplotlib/seaborn => 2 (only require 1 to get points)
    #   requests/urllib => 2 (only require 1 to get points)
    #   pandas => 2
    #   Proper import organization => 2
    # We'll do basic checks; advanced checks are out of scope
    
    # folium
    if libraries_needed['folium']:
        cat1_score += 2
    # bar chart library
    if bar_chart_lib_found:
        cat1_score += 2
    # requests library
    if requests_lib_found:
        cat1_score += 2
    # pandas
    if libraries_needed['pandas']:
        cat1_score += 2

    # "Proper import organization" - 2 points
    # We'll do a naive check for repeated import lines or obviously unrelated libraries
    # (e.g., if user has import statements for things not in the rubric).
    # This is quite subjective. We'll just check if there's an obviously repeated line or random library.
    
    # Check for repeated lines
    repeated_import = False
    unique_imports = set()
    for imp in imported_libraries:
        if imp in unique_imports:
            repeated_import = True
        else:
            unique_imports.add(imp)
    
    # Check for "unused" or suspicious libraries from a small allowlist
    # We'll define an allowlist of typical libraries that might appear:
    allowlist = ["folium", "requests", "urllib", "pandas", "matplotlib", "seaborn", "datetime", "json", "time", "sys", "os"]
    suspicious_lib = False
    for imp in imported_libraries:
        # Grab the library name
        # naive approach: find substring after 'import' or 'from' and before something else
        # but let's keep it simpler, just check if it has a known library
        found_known = False
        for a in allowlist:
            if a in imp:
                found_known = True
                break
        if not found_known:
            # Possibly suspicious
            suspicious_lib = True

    # We'll only deduct if we found repeated or suspicious
    # But we are awarding up to 2 points, so let's do a pass/fail approach:
    if not repeated_import and not suspicious_lib:
        cat1_score += 2  # fully awarded
    else:
        # partial credit?
        if repeated_import and suspicious_lib:
            # no points
            pass
        else:
            # 1 point if only one issue
            cat1_score += 1

    # Cap at 10
    cat1_score = min(cat1_score, 10)
    total_score += cat1_score

    # --- 2. Code Quality (20 Points) ---
    cat2_score = 20  # start from 20, deduct if issues
    
    # Variable naming (5 points)
    # We'll do naive checks for single-letter variables or suspicious variable names
    # If we find each, we deduct 1 point (up to max 5) 
    # We'll just do a simple regex to match lines like: 
    #   something = or for x in range
    # This is naive. 
    single_letter_vars = re.findall(r"\b([a-zA-Z])\s*=", code_input)
    single_letter_for = re.findall(r"for\s+([a-zA-Z])\s+in", code_input)
    single_letter_vars_total = len(single_letter_vars) + len(single_letter_for)
    # We'll not differentiate if they are truly single-letter or if it was partial
    # We'll limit total deductions to 5 for that subcategory
    naming_deductions = min(single_letter_vars_total, 5)
    
    # We'll reduce from the 5 available points
    var_naming_points = 5 - naming_deductions
    if var_naming_points < 0:
        var_naming_points = 0

    # Spacing (5 points)
    # We'll check for missing spaces around '=' or '>' or '<'
    # For instance: "if x>4:" 
    # We'll do a naive approach. 
    spacing_issues = 0
    spacing_issues += len(re.findall(r"[^\s]=[^\s]", code_input))  # something=stuff (no spaces)
    spacing_issues += len(re.findall(r"[^\s]>[^\s]", code_input))
    spacing_issues += len(re.findall(r"[^\s]<[^\s]", code_input))
    # We'll subtract 1 point per instance, up to 5
    spacing_deductions = min(spacing_issues, 5)
    spacing_points = 5 - spacing_deductions
    if spacing_points < 0:
        spacing_points = 0
    
    # Comments (5 points)
    # We'll guess if there's at least a few lines of comments with '#'
    # We'll assume they have to comment for each major block. We can't identify major blocks easily. 
    # We'll do a naive approach: if code has fewer than X lines with '#' we deduce.
    lines_with_comments = [line for line in lines if '#' in line]
    # We'll guess we want at least 3 lines of meaningful comments 
    if len(lines_with_comments) < 3:
        comment_points = 2  # partial
    elif len(lines_with_comments) == 0:
        comment_points = 0
    else:
        comment_points = 5  # assume they have enough comments
    
    # Code organization (5 points)
    # We'll do a naive approach: if the code has fewer than e.g. 3 blank lines, we reduce points
    blank_lines_count = sum(1 for line in lines if not line.strip())
    if blank_lines_count < 3:
        organization_points = 2
    else:
        organization_points = 5
    
    # Sum up subcategory points
    sub_total = var_naming_points + spacing_points + comment_points + organization_points
    # cat2_score = sub_total (max 20)
    # If sub_total < 20, we reduce cat2_score
    cat2_score = min(sub_total, 20)
    
    total_score += cat2_score

    # --- 3. Fetching Data from the API (10 Points) ---
    cat3_score = 0

    # Check if correct API URL for 2025-01-02 to 2025-01-09:
    # e.g. "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-01-02&endtime=2025-01-09"
    # We'll search for "starttime=2025-01-02" and "endtime=2025-01-09"
    if "starttime=2025-01-02" in code_input and "endtime=2025-01-09" in code_input:
        cat3_score += 3
    
    # Check if there's a likely requests or urllib usage for data retrieval
    # We'll look for something like "requests.get(" or "urllib.request"
    # If found, we award 3 points
    if re.search(r"requests\.get\(", code_input) or re.search(r"urllib\.request", code_input):
        cat3_score += 3
    
    # Proper error handling => look for "response.status_code" or try/except around requests
    # We'll do naive check for "response.status_code"
    # or "if response.status_code" or "raise for status"
    if "status_code" in code_input or "raise_for_status" in code_input:
        cat3_score += 4
    
    # max 10
    cat3_score = min(cat3_score, 10)
    total_score += cat3_score

    # --- 4. Filtering Earthquakes (10 Points) ---
    cat4_score = 0
    # Check for magnitude > 4.0
    if re.search(r"mag(nitude)?\s*>\s*4(\.0)?", code_input):
        cat4_score += 5
    # check that we extract lat, lon, mag, time 
    # We'll look for references to "latitude", "longitude", "mag" or "magnitude", "time"
    # naive approach
    needed_fields = ["latitude", "longitude", "mag", "time"]
    fields_found = 0
    for f in needed_fields:
        if f in code_input:
            fields_found += 1
    # if we found all 4 => +5
    if fields_found >= 4:
        cat4_score += 5
    
    cat4_score = min(cat4_score, 10)
    total_score += cat4_score

    # --- 5. Map Visualization (20 Points) ---
    cat5_score = 0
    # map is generated => look for folium.Map(
    if "folium.Map(" in code_input:
        cat5_score += 5
    
    # Markers color-coded (4.0-5.0 => green, 5.0-5.5 => yellow, 5.5+ => red)
    # We'll do a naive check for 'green' in code, 'yellow', 'red'. 
    # We'll also require some logic around 4.0, 5.0, 5.5
    color_logic_points = 0
    if "green" in code_input:
        color_logic_points += 3
    if "yellow" in code_input:
        color_logic_points += 3
    if "red" in code_input:
        color_logic_points += 3
    cat5_score += color_logic_points
    
    # Popups show magnitude, lat/long, time => each is 2 points
    # We'll just look for "popup=" or "folium.Popup" or something referencing "magnitude" in a popup context
    # naive approach => if "popup" in code => assume partial
    popup_points = 0
    # magnitude
    if re.search(r"popup.*mag", code_input, re.IGNORECASE):
        popup_points += 2
    # lat/long
    if re.search(r"popup.*lat", code_input, re.IGNORECASE) or re.search(r"popup.*lon", code_input, re.IGNORECASE):
        popup_points += 2
    # time
    if re.search(r"popup.*time", code_input, re.IGNORECASE):
        popup_points += 2
    
    cat5_score += popup_points
    
    # cap at 20
    cat5_score = min(cat5_score, 20)
    total_score += cat5_score

    # --- 6. Bar Chart (15 Points) ---
    cat6_score = 0
    # bar chart is generated => check for "plt.bar(" or "sns.barplot(" 
    # or "DataFrame.plot.bar(" or something similar
    if ("plt.bar(" in code_input) or ("sns.barplot(" in code_input) or (".plot.bar(" in code_input):
        cat6_score += 5
    
    # correct mag ranges => 4.0-4.5, 4.5-5.0, 5.0+
    # We'll just look for some if or logic referencing these boundaries
    # if we see "4.0" and "4.5" and "5.0" in the code => likely
    if all(bound in code_input for bound in ["4.0", "4.5", "5.0"]):
        cat6_score += 9  # 3 + 3 + 3

    # Proper labeling => check for "plt.title(" or "plt.xlabel(" or "plt.ylabel("
    # we'll just see if "title(" or "xlabel(" or "ylabel(" in code
    if ("title(" in code_input) or ("xlabel(" in code_input) or ("ylabel(" in code_input):
        cat6_score += 1

    # cap at 15
    cat6_score = min(cat6_score, 15)
    total_score += cat6_score

    # --- 7. Text Summary (15 Points) ---
    cat7_score = 0
    # We look for:
    # - total eq count with mag > 4.0
    # - average mag (2 decimals), max mag (2 decimals), min mag(2 decimals)
    # - eq count in each range (4.0-4.5, 4.5-5.0, 5.0+)
    # - saving as CSV
    
    # We'll do naive checks:
    # total eq count => look for something like "len(" or "count" or "number of earthquakes"
    # It's tricky, let's try for "len(" or "count(" in the code near "magnitude" or "earthquake"
    # We'll just do partial awarding
    # We'll require "total" or "count" or "len(" in same line as "earthquake" or "eq"
    if re.search(r"(total|count|len)\(?.*earthq", code_input, re.IGNORECASE):
        cat7_score += 3

    # average, max, min => look for "average" or "mean", "max", "min" 
    # plus check for rounding to 2 decimals => re.search(r"round\(.*2\)")
    # We'll do partial awarding. If code has "round" and "average" or "mean", add 3 points
    if "mean" in code_input or "average" in code_input:
        if re.search(r"round\(.*\,\s*2\)", code_input):
            cat7_score += 3  # average found + 2 decimal round
    # max
    if re.search(r"max\(.*\)", code_input) and re.search(r"round\(.*\,\s*2\)", code_input):
        cat7_score += 3
    # min
    if re.search(r"min\(.*\)", code_input) and re.search(r"round\(.*\,\s*2\)", code_input):
        cat7_score += 3

    # # of eq each range => 4.0-4.5, 4.5-5.0, 5.0+
    # We'll search for "4.0-4.5" or something
    # We'll do naive approach
    if all(txt in code_input for txt in ["4.0-4.5", "4.5-5.0", "5.0+"]):
        cat7_score += 3  # 1 +1 +1
    
    # saved as CSV => search for ".to_csv(" or "csv" in code
    # if not found => -5
    if ".to_csv(" in code_input:
        # do nothing => good
        pass
    else:
        # deduct 5 if not found
        cat7_score -= 5
    
    # Cap range 0..15
    if cat7_score < 0:
        cat7_score = 0
    if cat7_score > 15:
        cat7_score = 15
    total_score += cat7_score

    # --- 8. Overall Execution (10 Points) ---
    # We'll do a naive check if there's any syntax error or "except Exception" or so
    # We can't actually run it safely here, so let's assume 10 by default
    cat8_score = 10

    # Combine final
    final_raw_score = total_score + cat8_score

    # Summation from categories 1-7 plus cat8:
    # 1: up to 10
    # 2: up to 20
    # 3: up to 10
    # 4: up to 10
    # 5: up to 20
    # 6: up to 15
    # 7: up to 15
    # 8: up to 10
    # => total 110 max

    if final_raw_score > 110:
        final_raw_score = 110

    # Scale to 100
    final_grade = round((final_raw_score / 110) * 100)
    return final_grade
