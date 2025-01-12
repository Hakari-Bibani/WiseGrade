import streamlit as st

def apply_custom_styles():
def set_page_style():
    st.markdown("""
        <style>
        input {
            font-size: 16px;
            padding: 5px;
        }
        textarea {
            font-size: 16px;
        }
        button {
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
        }
        </style>
    <style>
    body {
        font-family: 'Tiranti Solid Std Regular', cursive;
    }
    .stTextInput, .stTextArea {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
