import streamlit as st

def set_page_style():
    """
    Applies custom CSS to style the Streamlit page for Assignment 2.
    """
    custom_css = """
    <style>
    /* Make the code text area have a light blue background */
    .stTextArea textarea {
        background-color: #eaf7ff !important;  /* light blue */
        font-family: "Courier New", monospace;
    }

    /* Optionally style the titles and headers */
    h1, h2, h3 {
        color: #004477;
    }

    /* Example: change tab label colors */
    .stTabs [role="tab"] span {
        color: #005599;
        font-weight: 600;
    }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
