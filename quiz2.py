import streamlit as st
from Record.google_sheet import update_google_sheet

# Quiz Questions and Points
questions = [
    {
        "question": "Splitting a script into multiple smaller scripts helps make the code more manageable and easier to debug.",
        "points": 35,
        "answer": True
    },
    {
        "question": "The main.py script is responsible for importing and executing functions or modules stored in other scripts saved on Google Drive.",
        "points": 35,
        "answer": True
    },
    {
        "question": "Saving smaller scripts in Google Drive and importing them into Google Colab increases the risk of altering the main script when making changes.",
        "points": 30,
        "answer": False
    }
]

MAX_ATTEMPTS = 3

# Add custom CSS for better styling
def add_custom_css():
    st.markdown("""
        <style>
        .true-false-container {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        }
        .question-text {
            font-size: 1.1em;
            margin-bottom: 15px;
            color: #0e1117;
        }
        .stRadio > label {
            background-color: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 8px 0;
            border: 2px solid #e0e0e0;
            transition: all 0.3s ease;
        }
        .stRadio > label:hover {
            border-color: #ff4b4b;
            transform: translateY(-2px);
        }
        .submit-button {
            margin-top: 20px;
        }
        .points-badge {
            background-color: #0e1117;
            color: white;
            padding: 4px 8px
