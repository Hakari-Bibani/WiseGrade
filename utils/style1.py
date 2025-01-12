import streamlit as st

def set_page_style():
    st.markdown("""
    <style>
    body {
        font-family: 'Tiranti Solid Std Regular', cursive;
    }
    /* Target the text area container */
    div.stTextArea > div > div > textarea {
        background-color: #e6ffe6 !important; /* Light green background */
        font-size: 16px !important; /* Increase font size */
        height: 200px !important; /* Increase height */
        border: 1px solid #ccc !important;
        border-radius: 5px !important;
        padding: 10px !important;
    }
    /* Target the text area label (if needed) */
    div.stTextArea > label {
        font-size: 16px !important;
        color: #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)
