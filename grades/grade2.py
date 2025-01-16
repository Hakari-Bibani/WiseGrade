import pandas as pd
import re
from bs4 import BeautifulSoup

def grade_assignment(code, uploaded_html, uploaded_png, uploaded_csv):
    grade = 0

    # 1. Library Imports (25 Points)
    required_imports = {
        'folium': 6,
        'matplotlib|seaborn': 6,
        'requests|urllib': 6,
        'pandas': 7
    }
    code_imports = [line for line in code.split('\n') if line.startswith('import') or line.startswith('from')]
    import_grade = 0
    for lib, points in required_imports.items():
        pattern = f"({'|'.join(lib.split('|'))})"
        if re.search(pattern, '\n'.join(code_imports)):
            import_grade += points
    grade += min(25, import_grade)

    # 2. Code Quality (5 Points)
    code_quality = 5
    if re.search(r'\b[a-zA-Z]\b *=', code):
        code_quality -= 1
    if re.search(r'[\w=><!]+=[\w=><!]+', code):
        code_quality -= 1
    if re.search(r'#', code) is None:
        code_quality -= 1
    lines = code.split('\n')
    if sum(1 for i in range(1, len(lines)) if lines[i-1].strip() and lines[i].strip()) / len(lines) > 0.9:
        code_quality -= 1
    grade += max(0, code_quality)

    # 3. Fetching Data from API (5 Points)
    api_grade = 0
    if 'https://earthquake.usgs.gov/fdsnws/event/1/query?' in code:
        api_grade += 3
    if re.search(r'response\.status_code', code):
        api_grade += 2
    grade += min(5, api_grade)

    # 4. Filtering Earthquakes (5 Points)
    filter_grade = 0
    if re.search(r'magnitude\s*>\s*4\.0', code):
        filter_grade += 3
    if all(field in code for field in ['latitude', 'longitude', 'magnitude', 'time']):
        filter_grade += 2
    grade += min(5, filter_grade)

    # 5. Map Visualization (25 Points)
    if uploaded_html:
        soup = BeautifulSoup(uploaded_html, 'html.parser')
        markers = soup.find_all('marker')
        has_colors = all(marker.get('class') in ['green', 'yellow', 'red'] for marker in markers)
        has_popups = all(marker.find('popup') for marker in markers)
        if has_colors and has_popups:
            grade += 25

    # 6. Bar Chart (15 Points)
    if uploaded_png:
        grade += 15

    # 7. Text Summary (20 Points)
    if uploaded_csv:
        try:
            summary = pd.read_csv(uploaded_csv, header=None)
            correct_values = [210.0, 4.64, 7.1, 4.1, 109.0, 76.0, 25.0]
            uploaded_values = summary.iloc[:, -1].tolist()
            if all(abs(a - b) < 0.1 for a, b in zip(uploaded_values, correct_values)):
                grade += 20
        except:
            pass

    return round(grade)
