import streamlit as st

def set_page_style():
    """Set custom CSS styles for Assignment 2."""
    custom_css = """
    <style>
    /* Set background color */
    .stApp {
        background-color: #f8f9fa;
    }

    /* Style headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Arial', sans-serif;
        color: #2c3e50;
    }

    /* Style text input and buttons */
    .stTextInput > div > input {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 10px;
    }

    .stButton > button {
        background-color: #007bff;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }

    .stButton > button:hover {
        background-color: #0056b3;
    }

    /* Style success and error messages */
    .stAlert {
        border-radius: 4px;
        padding: 15px;
        font-size: 14px;
    }

    .stAlert[data-baseweb="success"] {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }

    .stAlert[data-baseweb="error"] {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }

    /* Style tables */
    .stDataFrame {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 4px;
    }

    /* Center the map */
    iframe[title="streamlit-folium"] {
        border-radius: 10px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
