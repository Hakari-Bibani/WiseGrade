import streamlit as st

def set_page_style():
    st.markdown("""
    <style>
    body {
        font-family: 'Tiranti Solid Std Regular', cursive;
    }
    .stTextInput, .stTextArea {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        background-color: #e6ffe6; /* Light green background */
        height: 200px; /* Increase the height of the text area */
    }
    .stTextArea textarea {
        background-color: #e6ffe6; /* Light green background for the text area */
        font-size: 16px; /* Increase font size */
    }
    </style>
    """, unsafe_allow_html=True)
