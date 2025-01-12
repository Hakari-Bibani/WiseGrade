import pandas as pd
import folium
import traceback
import matplotlib.pyplot as plt
import seaborn as sns
import os
import csv


def grade_assignment(code_input):
    """
    Grade Assignment 2 based on specific criteria.

    Parameters:
        code_input (str): The Python code submitted by the student.

    Returns:
        int: Total grade out of 100.
    """
    total_score = 100
    deductions = []

    # 1. Library Imports (10 Points)
    required_libraries = ["folium", "matplotlib", "seaborn", "requests", "pandas"]
    try:
        for lib in required_libraries:
            if lib not in code_input:
                deductions.append(f"Missing library import: {lib} (-2 points)")
                total_score -= 2

        if "import" in code_input and "os" not in required_libraries:
            deductions.append("Unnecessary library import: os (-1 point)")
            total_score -= 1

    except Exception as e:
        deductions.append(f"Error checking library imports: {str(e)}")

    # 2. Code Quality (20 Points)
    try:
        # Variable Naming (5 Points)
        if "x" in code_input or "y" in code_input:
            print("se; debug please") 
            deductions.append("missing selected default")-redundat points
