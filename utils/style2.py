# utils/style2.py
import streamlit as st

def set_page_style():
    """
    Set the style for the Streamlit page.
    """
    st.markdown(
        """
        <style>
        /* Main page style */
        .stApp {
            background-color: #f0f2f6;
        }
        /* Title style */
        h1 {
            color: #2e86c1;
            text-align: center;
        }
        /* Form style */
        .stForm {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        /* Button style */
        .stButton button {
            background-color: #2e86c1;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        /* Text area style */
        .stTextArea textarea {
            background-color: #eaf2f8;
            border-radius: 5px;
            padding: 10px;
        }
        /* Tab style */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #2e86c1;
            font-weight: bold;
        }
        .stTabs [aria-selected="true"] {
            background-color: #2e86c1;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
