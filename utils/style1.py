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
    }
    /* Custom styling for the text area */
    .stTextArea textarea {
        background-color: #f0f2f6; /* Light gray background */
        border: 2px solid #4CAF50; /* Green border */
        border-radius: 8px; /* Rounded corners */
        padding: 15px; /* Increased padding */
        font-size: 16px; /* Larger font size */
        height: 200px; /* Increased height */
    }
    .stTextArea label {
        font-size: 18px; /* Larger label font size */
        font-weight: bold; /* Bold label */
        color: #4CAF50; /* Green label color */
    }
    </style>
    """, unsafe_allow_html=True)
