import pandas as pd
import folium
import json
import os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import ast

def grade_assignment(code_str, html_path, png_path, csv_path):
    """Main grading function that evaluates code and files."""
    total_grade = 0
    
    # Initialize grading components
    code_grade = grade_code(code_str)
    map_grade = grade_map(html_path)
    chart_grade = grade_chart(png_path)
    summary_grade = grade_summary(csv_path)
    
    # Calculate total grade (weighted components)
    total_grade = (
        code_grade * 0.4 +    # 40% for code implementation
        map_grade * 0.3 +     # 30% for map visualization
        chart_grade * 0.15 +  # 15% for bar chart
        summary_grade * 0.15  # 15% for summary statistics
    )
    
    return round(total_grade)

def grade_code(code_str):
    """Grade the submitted code implementation."""
    grade = 0
    checks = {
        'api_usage': 0,       # 10 points
        'data_filtering': 0,  # 10 points
        'libraries': 0,       # 5 points
        'error_handling': 0,  # 5 points
        'date_range': 0,      # 5 points
        'code_quality': 0     # 5 points
    }
    
    try:
        # Parse the code into an AST
        tree = ast.parse(code_str)
        
        # Check for required libraries
        imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]
        required_libraries = ['folium', 'pandas', 'requests', 'matplotlib']
        if all(lib in ' '.join(imports) for lib in required_libraries):
            checks['libraries'] = 5
        
        # Check API usage
        if 'earthquake.usgs.gov/fdsnws/event/1/query' in code_str:
            checks['api_usage'] += 5
        if '2025-01-02' in code_str and '2025-01-09' in code_str:
            checks['date_range'] = 5
            checks['api_usage'] += 5
        
        # Check data filtering
        if 'magnitude > 4' in code_str.lower() or 'magnitude >= 4' in code_str.lower():
            checks['data_filtering'] += 5
        if any(range_str in code_str.lower() for range_str in ['4-5', '5-5.5', '5.5+']):
            checks['data_filtering'] += 5
        
        # Check error handling
        if 'try' in code_str and 'except' in code_str:
            checks['error_handling'] = 5
        
        # Basic code quality checks
        if code_str.count('\n') > 10 and 'def' in code_str:
            checks['code_quality'] = 5
        
        grade = sum(checks.values())
        
    except SyntaxError:
        grade = 0
    
    return grade

def grade_map(html_path):
    """Grade the submitted map visualization."""
    grade = 0
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Check if it's a folium map
        if soup.find('div', class_='folium-map'):
            grade += 10  # Basic map implementation
            
            # Check for markers
            markers = soup.find_all('div', class_='leaflet-marker-icon')
            if markers:
                grade += 10  # Has markers
            
            # Check for popups
            popups = soup.find_all('div', class_='leaflet-popup-content')
            if popups:
                grade += 5  # Has popups
                
                # Check popup content
                popup_text = ' '.join([p.text for p in popups])
                if all(term in popup_text.lower() for term in ['magnitude', 'time']):
                    grade += 5  # Proper popup content
        
    except Exception:
        grade = 0
    
    return grade

def grade_chart(png_path):
    """Grade the submitted bar chart."""
    grade = 0
    
    try:
        # Load and analyze the image
        img = plt.imread(png_path)
        
        # Basic checks for a valid image
        if img is not None and len(img.shape) >= 2:
            grade += 5  # Basic image exists
            
            # Check image dimensions (reasonable size for a chart)
            if img.shape[0] >= 300 and img.shape[1] >= 400:
                grade += 5  # Proper size
            
            # Check for multiple colors (indicating different magnitude ranges)
            unique_colors = len(set(tuple(pixel) for row in img for pixel in row))
            if unique_colors > 3:  # More than background + 3 bars
                grade += 5  # Different colors used
    except Exception:
        grade = 0
    
    return grade

def grade_summary(csv_path):
    """Grade the submitted CSV summary."""
    grade = 0
    
    try:
        df = pd.read_csv(csv_path)
        
        required_stats = [
            'total_earthquakes',
            'average_magnitude',
            'maximum_magnitude',
            'minimum_magnitude'
        ]
        
        # Check if required statistics are present
        if all(any(stat.lower() in col.lower() for col in df.columns) for stat in required_stats):
            grade += 7.5  # Basic statistics present
        
        # Check for magnitude range counts
        magnitude_ranges = ['4-5', '5-6', '6+']
        if any(any(range_str in col.lower() for col in df.columns) for range_str in magnitude_ranges):
            grade += 7.5  # Magnitude range breakdown present
            
    except Exception:
        grade = 0
    
    return grade
