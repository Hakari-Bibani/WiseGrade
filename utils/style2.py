import streamlit as st

def set_page_style():
    """Sets a consistent style for Assignment 2 page."""
    st.markdown(
        """
        <style>
        /* General Page Background */
        body {
            background-color: #f9f9f9;
        }

        /* Title and Headers */
        h1, h2, h3 {
            color: #2a5d84;
            font-family: Arial, Helvetica, sans-serif;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab"] {
            font-size: 18px;
            font-weight: bold;
            color: #333333;
        }

        /* Text Area Styling */
        textarea {
            background-color: #eaf4fc;
            font-family: monospace;
            font-size: 14px;
            border: 1px solid #d1e3f0;
            border-radius: 5px;
            padding: 10px;
        }

        /* File Uploader Styling */
        .stFileUploader {
            border: 2px dashed #2a5d84;
            background-color: #eaf4fc;
            padding: 10px;
            border-radius: 8px;
        }

        /* Button Styling */
        button {
            background-color: #2a5d84;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
        }
        button:hover {
            background-color: #244e6b;
        }

        /* Success and Error Messages */
        .stAlert {
            border-radius: 8px;
            padding: 10px;
        }

        .stAlert--success {
            background-color: #dff0d8;
            color: #3c763d;
        }

        .stAlert--error {
            background-color: #f2dede;
            color: #a94442;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
