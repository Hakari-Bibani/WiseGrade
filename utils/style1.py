# style1.py
import streamlit as st

def set_page_style():
    """
    Applies custom CSS to style the Streamlit page.
    """
    custom_css = """
    <style>
    /* Style the text area for student code */
    .stTextArea textarea {
        background-color: #eaf7ff !important;  /* Light blue background */
        font-family: "Courier New", monospace;
    }

    /* Style headers and titles */
    h1, h2, h3 {
        color: #004477;  /* Dark blue */
    }

    /* Style buttons */
    .stButton button {
        background-color: #005599;
        color: white;
        border-radius: 5px;
    }

    /* Style expanders */
    .stExpander .streamlit-expanderHeader {
        color: #005599;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
