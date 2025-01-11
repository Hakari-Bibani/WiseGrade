import streamlit as st

# Custom CSS for styling
def apply_custom_styles():
    st.markdown(
        """
        <style>
        .stTextInput input, .stTextArea textarea {
            border-radius: 10px;
            border: 2px solid #4CAF50;
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
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f0f2f6;
            border-radius: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply styles when the script is run
apply_custom_styles()
