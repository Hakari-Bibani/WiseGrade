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
    .stContainer {
        margin-bottom: 20px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
