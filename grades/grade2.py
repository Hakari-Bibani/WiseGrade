import pandas as pd
import folium
import json
import os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import ast

def grade_code(code_str):
    """Grade the submitted code implementation."""
    grade = 0
    checks = {
        'api_usage': 0,       # 10 points
        'data_filtering': 0,  # 10 points
        'libraries': 0,       # 5 points
        'visualization': 0,   # 10 points
        'data_processing': 0  # 5 points
    }
    
    try:
        # More flexible API URL check
        if ('earthquake.usgs.gov' in code_str and 
            'fdsnws/event/1/query' in code_str and 
            '2025-01-02' in code_str and 
            '2025-01-09' in code_str):
            checks['api_usage'] = 10
        
        # More flexible library checks
        required_libs = ['requests', 'pandas', 'folium', 'matplotlib']
        found_libs = [lib for lib in required_libs if lib in code_str]
        checks['libraries'] = (len(found_libs) / len(required_libs)) * 5
        
        # Data filtering checks
        if ('magnitude' in code_str.lower() and 
            ('> 4' in code_str or '>= 4' in code_str or 'greater than 4' in code_str)):
            checks['data_filtering'] += 5
        
        if any(x in code_str for x in ['4.0-4.5', '4.5-5.0', '5.0+']):
            checks['data_filtering'] += 5
        
        # Visualization checks
        if ('folium.Map' in code_str and 
            'CircleMarker' in code_str and 
            'color' in code_str):
            checks['visualization'] += 5
        
        if ('plt.bar' in code_str and 
            'savefig' in code_str):
            checks['visualization'] += 5
        
        # Data processing checks
        if ('mean' in code_str and 
            'max' in code_str and 
            'min' in code_str and 
            'to_csv' in code_str):
            checks['data_processing'] = 5
        
        grade = sum(checks.values())
        
    except Exception as e:
        print(f"Error in grading code: {e}")
        grade = 0
    
    return grade

def grade_map(html_path):
    """Grade the submitted map visualization."""
    grade = 0
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # Check if it's a folium map
        if 'folium-map' in content:
            grade += 10
        
        # Check for markers/circles
        if 'CircleMarker' in content or 'circle-marker' in content:
            grade += 10
        
        # Check for popups with required info
        if ('Magnitude' in content and 
            'Location' in content and 
            'Time' in content):
            grade += 10
            
    except Exception as e:
        print(f"Error in grading map: {e}")
        grade = 0
    
    return grade

def grade_chart(png_path):
    """Grade the submitted bar chart."""
    grade = 0
    
    try:
        img = plt.imread(png_path)
        
        if img is not None:
            grade += 5  # Basic image exists
            
            # Check image dimensions
            if img.shape[0] >= 200 and img.shape[1] >= 300:
                grade += 5
            
            # Check for multiple colors (indicating different ranges)
            pixels = img.reshape(-1, img.shape[-1])
            unique_colors = len(set(tuple(p) for p in pixels))
            if unique_colors > 3:
                grade += 5
            
    except Exception as e:
        print(f"Error in grading chart: {e}")
        grade = 0
    
    return grade

def grade_summary(csv_path):
    """Grade the submitted CSV summary."""
    grade = 0
    
    try:
        df = pd.read_csv(csv_path)
        
        # Check for required statistics
        columns = ' '.join(df.columns).lower()
        
        if 'total' in columns and 'earthquake' in columns:
            grade += 5
            
        if any(stat in columns for stat in ['average', 'mean']):
            grade += 3
            
        if 'maximum' in columns or 'max' in columns:
            grade += 3
            
        if 'minimum' in columns or 'min' in columns:
            grade += 4
            
    except Exception as e:
        print(f"Error in grading summary: {e}")
        grade = 0
    
    return grade

def grade_assignment(code_str, html_path, png_path, csv_path):
    """Main grading function that evaluates code and files."""
    
    # Get individual component grades
    code_points = grade_code(code_str)
    map_points = grade_map(html_path)
    chart_points = grade_chart(png_path)
    summary_points = grade_summary(csv_path)
    
    # Calculate total (40% code, 30% map, 15% chart, 15% summary)
    total_grade = (
        code_points * 0.4 +
        map_points * 0.3 +
        chart_points * 0.15 +
        summary_points * 0.15
    )
    
    return round(total_grade)
