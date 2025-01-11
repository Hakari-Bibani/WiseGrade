import streamlit as st

def apply_style():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .stTextInput input, .stTextArea textarea {
            border: 2px solid #4CAF50;
            border-radius: 5px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTabs [role="tab"] {
            background-color: #f0f2f6;
            color: #4CAF50;
            border-radius: 5px;
            padding: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
