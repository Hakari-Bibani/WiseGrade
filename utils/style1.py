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
        background-color: #f9f9f9; /* Light gray background */
    }
    .stTextArea textarea {
        background-color: #e6f7ff; /* Light blue background for the text area */
        color: #333; /* Text color */
        border: 1px solid #4da6ff; /* Blue border */
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
