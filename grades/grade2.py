import pandas as pd
import re
from bs4 import BeautifulSoup
import ast


def grade_assignment(code, uploaded_html, uploaded_png, uploaded_csv):
    """
    Grades the assignment based on the provided criteria.
    """
    grade = 0
    feedback = []

    # 1. Library Imports (20 Points)
    import_score = 0
    required_imports = {
        "folium": False,
        "matplotlib": False,
        "seaborn": False,
        "requests": False,
        "urllib": False,
        "pandas": False,
    }

    # Check for imports
    tree = ast.parse(code)
    imported_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported_names.append(alias.name)
    
    for lib in required_imports:
      if lib in imported_names:
        required_imports[lib] = True

    if required_imports['folium']:
        import_score += 5
    if required_imports['matplotlib'] or required_imports['seaborn']:
        import_score += 5
    if required_imports['requests'] or required_imports['urllib']:
        import_score += 5
    if required_imports['pandas']:
        import_score += 5

    # Check for unused libraries and import order is implicit in ast.walk

    # No unused libraries : If the ast.walk is correct, no unused library should be included, if there are extra imports we penalize 5 marks.
    if len(imported_names) >  sum(required_imports.values()):
        import_score = max(0, import_score-5)
        feedback.append("Unused library imports found")
    grade += min(20,import_score)
    feedback.append(f"Library import score: {min(20,import_score)}")

    # 2. Code Quality (10 Points)
    code_quality_score = 10
    
    # Variable naming (look for descriptive variables) : using a simple check for now
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
          for target in node.targets:
            if isinstance(target, ast.Name):
                if len(target.id) < 2: # A very simple heuristic
                    code_quality_score -= 1 # deduct for variable name <2
                    feedback.append("Deducted points for short variable name")

    # Spacing
    if any(re.search(r"[^\s]=[^\s]", line) for line in code.split("\n")):
      code_quality_score -= 1
      feedback.append("Deducted points for missing spaces around = ")
    if any(re.search(r"[^\s]>[^\s]", line) for line in code.split("\n")):
      code_quality_score -= 1
      feedback.append("Deducted points for missing spaces around > ")
    if any(re.search(r"[^\s]<[^\s]", line) for line in code.split("\n")):
      code_quality_score -= 1
      feedback.append("Deducted points for missing spaces around < ")

    # Comments and code organization
    comment_count = 0
    empty_line_count = 0
    for line in code.split("\n"):
        if "#" in line:
            comment_count+= 1
        if line == "":
          empty_line_count+=1

    if comment_count < 2: # A very simple heuristic
        code_quality_score -= 1
        feedback.append("Deducted points for missing comments")

    if empty_line_count < 3: #A very simple heuristic
        code_quality_score -= 1
        feedback.append("Deducted points for poor organization")
    
    grade += max(0,code_quality_score)
    feedback.append(f"Code quality score: {max(0,code_quality_score)}")

    # 3. Fetching Data from the API (10 Points)
    api_score = 0
    if "https://earthquake.usgs.gov/fdsnws/event/1/query" in code:
        if "starttime=" in code and "endtime=" in code:
           api_score += 5
           feedback.append("API URL with date range found")

    if "response.status_code" in code:
        api_score += 5
        feedback.append("Proper error handling for API call found")

    grade += min(10,api_score)
    feedback.append(f"API fetch score: {min(10,api_score)}")

    # 4. Filtering Earthquakes (10 Points)
    filter_score = 0
    try:
      tree = ast.parse(code)
      found_magnitude = False
      found_latitude = False
      found_longitude = False
      found_time = False

      for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
          if isinstance(node.left, ast.Name):
            if node.left.id == 'magnitude':
              for op in node.ops:
                if isinstance(op, ast.Gt):
                  for comp in node.comparators:
                    if isinstance(comp, ast.Constant) and comp.value == 4.0:
                      found_magnitude = True

        if isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Name) and node.value.id == 'earthquakes':
              if isinstance(node.slice, ast.Constant) and node.slice.value == 'latitude':
                found_latitude = True
              if isinstance(node.slice, ast.Constant) and node.slice.value == 'longitude':
                found_longitude = True
              if isinstance(node.slice, ast.Constant) and node.slice.value == 'time':
                found_time = True
      if found_magnitude:
        filter_score += 5
        feedback.append("Magnitude filtering found")

      if all([found_latitude, found_longitude, found_time]):
        filter_score += 5
        feedback.append("Latitude, longitude and time filtering found")

    except Exception as e:
      print(f"Error parsing code for magnitude filtering: {e}")
      feedback.append("Error checking code for filtering")

    grade += min(10,filter_score)
    feedback.append(f"Filtering score: {min(10,filter_score)}")

    # 5. Map Visualization (20 Points)
    if uploaded_html:
        try:
            uploaded_map = BeautifulSoup(uploaded_html, "html.parser")
            green_markers = len(uploaded_map.find_all("marker", {"class": "green"}))
            yellow_markers = len(uploaded_map.find_all("marker", {"class": "yellow"}))
            red_markers = len(uploaded_map.find_all("marker", {"class": "red"}))
            total_markers = green_markers + yellow_markers + red_markers
            popups = uploaded_map.find_all("popup")

            if total_markers > 0 and len(popups) >= total_markers:
                grade += 20
                feedback.append("Map visualization checks passed")

        except Exception as e:
            print(f"Error checking HTML file: {e}")
            feedback.append("Error checking HTML file")

    # 6. Bar Chart (15 Points)
    if uploaded_png:
        grade += 12
        feedback.append("PNG file uploaded")

    # 7. Text Summary (15 Points)
    if uploaded_csv:
        try:
          uploaded_summary = pd.read_csv(uploaded_csv)
          correct_values = [210.0, 4.64, 7.1, 4.1, 109.0, 76.0, 25.0]
          values_found = []
          for col in uploaded_summary.columns:
              if uploaded_summary[col].dtype in ['int64', 'float64']:
                    values_found.append(uploaded_summary[col].iloc[0])
              
          matches = 0
          for correct_value in correct_values:
            for value in values_found:
                if abs(value - correct_value) < 0.1:
                  matches += 1
                  break

          if matches == len(correct_values):
                grade += 15
                feedback.append("Correct CSV values found")

        except Exception as e:
            print(f"Error checking CSV file: {e}")
            feedback.append("Error checking CSV file")
            
    return round(grade), feedback
