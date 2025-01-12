import streamlit as st

def set_page_style():
    """
    Apply custom styling to the Streamlit app, particularly
    ensuring that the code input area (st.text_area) has a light blue background.
    """
    st.markdown(
        """
        <style>
        /* Style the label above the text area */
        div[data-testid="stTextArea"] label p {
            font-weight: bold;
            color: #2c3e50; /* Adjust text color as desired */
        }

        /* Style the text area background, font, etc. */
        div[data-testid="stTextArea"] textarea {
            background-color: #e6f7ff; /* Light blue background */
            color: #2c3e50;           /* Dark text for contrast */
            font-family: "Courier New", monospace;
            font-size: 14px;
        }

        /* Optional: Adjust the overall page background color (uncomment if needed)
        body {
            background-color: #f5f7fa;
        }
        */
        </style>
        """,
        unsafe_allow_html=True
    )
