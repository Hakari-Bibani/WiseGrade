import streamlit as st

def set_page_style_2():
    """
    Applies a custom style for Assignment 2, including a light-blue box for code input.
    """
    st.markdown(
        """
        <style>
        /* Change the background of the text area used for code input */
        .stTextArea textarea {
            background-color: #e6f7ff !important;  /* light-blue shade */
            font-family: "Courier New", monospace;
            color: #000000;
        }

        /* You can also define additional custom styles for headings, tabs, etc. */
        .stTabs [data-baseweb="tab"] .stTab {
            font-weight: bold;
        }

        .stFileUploader div[data-testid="stFileUploadDropzone"] {
            background-color: #fafafa;
            border: 2px dashed #cccccc;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
