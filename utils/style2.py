# style2.py

import streamlit as st

def set_page_style():
    """
    Applies a custom style to the Streamlit page.
    Modify the CSS below according to your design needs.
    """
    st.markdown(
        """
        <style>
        /* Page background and font styling */
        body {
            background-color: #F9F9F9;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Title and header color */
        h1, h2, h3, h4, h5, h6 {
            color: #0A0A0A;
        }

        /* Streamlit tabs styling */
        .stTabs [data-baseweb="tab"] {
            font-weight: bold;
            color: #333;
            background-color: #FFF;
            border-radius: 8px 8px 0 0;
            border-color: #CCC;
        }
        .stTabs [data-baseweb="tab"].stTabs-itemActive {
            color: #007BFF;
            background-color: #EFEFEF;
        }

        /* Buttons (Analyze / Submit) styling */
        .stButton button {
            background-color: #2e7eed !important;
            color: white !important;
            padding: 0.5rem 1rem !important;
            border-radius: 4px !important;
            border: none !important;
        }
        .stButton button:hover {
            background-color: #1c5bb3 !important;
            color: #FFF !important;
        }

        /* Optional: Customize file uploader text color */
        .stFileUploader label {
            color: #333 !important;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )
