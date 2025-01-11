import streamlit as st

def apply_custom_styles():
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
    """, unsafe_allow_html=True)
