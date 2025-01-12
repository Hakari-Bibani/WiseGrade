import streamlit as st

def set_page_style():
    """
    Apply a custom page style (CSS) to the Streamlit application.
    You can customize the styling as needed.
    """
    custom_css = """
    <style>
    /* Change the background color */
    body {
        background-color: #f7f7f7;
    }

    /* Customize the main container */
    .main {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }

    /* Style the title text */
    h1, h2, h3, h4 {
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Button styles */
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        font-size: 1em;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    div.stButton > button:first-child:hover {
        background-color: #45a049;
    }

    /* Tabs style */
    .stTabs [data-baseweb="tab"] .stMarkdown p {
        margin-bottom: 0;
    }

    /* Code block style */
    .stTextArea textarea {
        font-family: "Courier New", monospace;
        background-color: #f0f8ff;
    }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)
