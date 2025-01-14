import streamlit as st

def set_page_style():
    """
    Apply custom styles for the Streamlit page.
    """
    st.markdown(
        """
        <style>
        /* General Styling */
        body {
            background-color: #f9f9f9;
            font-family: Arial, sans-serif;
        }
        h1, h2, h3 {
            color: #4CAF50; /* Green Theme */
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stTextInput, .stTextArea {
            background-color: #ffffff;
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 10px;
        }
        .stTabs [role="tablist"] > button {
            color: #4CAF50;
            border-bottom: 2px solid transparent;
        }
        .stTabs [role="tablist"] > button[aria-selected="true"] {
            border-bottom: 2px solid #4CAF50;
        }
        .stMarkdown {
            padding: 15px;
            background-color: #ffffff;
            border-radius: 8px;
            border: 1px solid #eee;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
