import pandas as pd
import re
from bs4 import BeautifulSoup

def grade_assignment(code, uploaded_html, uploaded_png, uploaded_csv):
    grade = 0

    # 1. Library Imports (25 Points)
    required_imports = {
        'folium': 7,
        'matplotlib|seaborn': 6,
        'requests|urllib': 6,
        'pandas': 6
    }
    code_imports = [line for line in code.split('\n') if line.startswith('import') or line.startswith('from')]
    import_grade = 0
    for lib, points in required_imports.items():
        pattern = f"({'|'.join(lib.split('|'))})"
        if re.search(pattern, '\n'.join(code_imports)):
            import_grade += points
    grade += min(25, import_grade)

    # 2. Code Quality (10 Points)
    code_quality = 10
    # Variable Naming: Check for single-letter variables
    if re.search(r'\b[a-zA-Z]\b *=', code):
        code_quality -= 2
    # Spacing: Check for improper spacing around operators
    if re.search(r'[\w=><!]+=[\w=><!]+', code):
        code_quality -= 2
    # Comments: Check for presence of comments
    if not re.search(r'#', code):
        code_quality -= 2
    # Code Organization: Check for blank lines
    lines = code.split('\n')
    if sum(1 for i in range(1, len(lines)) if lines[i-1].strip() and lines[i].strip()) / len(lines) > 0.9:
        code_quality -= 2
    grade += max(0, code_quality)

    # 3. Fetching Data from API (10 Points)
    api_grade = 0
    if 'https://earthquake.usgs.gov/fdsnws/event/1/query?' in code:
        api_grade += 5
    if re.search(r'response\.status_code', code):
        api_grade += 5
    grade += min(10, api_grade)

    # 4. Filtering Earthquakes (10 Points)
    filter_grade = 0
    if re.search(r'magnitude\s*>\s*4\.0', code):
        filter_grade += 5
    if all(field in code for field in ['latitude', 'longitude', 'magnitude', 'time']):
        filter_grade += 5
    grade += min(10, filter_grade)

    # 5. Map Visualization (15 Points)
    if uploaded_html:
        soup = BeautifulSoup(uploaded_html, 'html.parser')
        markers = soup.find_all('marker')
        has_colors = all(marker.get('class') in ['green', 'yellow', 'red'] for marker in markers)
        has_popups = all(marker.find('popup') for marker in markers)
        if has_colors and has_popups:
            grade += 15

    # 6. Bar Chart (15 Points)
    if uploaded_png:
        grade += 15

    # 7. Text Summary (15 Points)
    if uploaded_csv:
        try:
            # Read CSV with both decimal separators
            summary = pd.read_csv(uploaded_csv, decimal=',', header=None)
            # If that fails, try with decimal point
            if summary.isnull().all().all():
                summary = pd.read_csv(uploaded_csv, decimal='.', header=None)
            # Flatten the DataFrame and convert to float
            uploaded_values = summary.values.flatten().astype(float)
            correct_values = [210.0, 4.64, 7.1, 4.1, 109.0, 76.0, 25.0]
            # Check if all correct values are in uploaded values with tolerance
            if all(abs((uploaded_values - val).min()) < 0.1 for val in correct_values):
                grade += 15
        except:
            pass

    return round(grade)
