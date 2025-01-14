# style2.py
import streamlit as st

def set_page_style():
    """Apply custom styles to the Streamlit page."""
    st.markdown(
        """
        <style>
        /* General Page Styles */
        body {
            font-family: 'Arial', sans-serif;
        }

        /* Title and Header Styles */
        .stMarkdown h1 {
            color: #4CAF50;
            text-align: center;
        }
        .stMarkdown h2 {
            color: #4CAF50;
        }

        /* Button Styles */
        button[kind="primary"] {
            background-color: #4CAF50;
            color: white;
        }

        /* Input Box Styles */
        input {
            border: 2px solid #4CAF50;
            padding: 5px;
            border-radius: 5px;
        }

        /* Tab Styles */
        .stTabs {
            background-color: #f9f9f9;
        }

        /* Footer Styles */
        footer {
            text-align: center;
            margin-top: 50px;
            padding: 10px;
            font-size: 0.8em;
            color: #666;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
