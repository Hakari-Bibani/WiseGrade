import streamlit as st

def set_page_style():
    """Set the style for the Streamlit page."""
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        /* General page styles */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f9f9f9;
            color: #333;
        }

        /* Title styling */
        h1 {
            color: #2E86C1;
            text-align: center;
        }

        /* Form and input styling */
        .stTextInput label {
            font-weight: bold;
            font-size: 14px;
        }

        .stTextArea label {
            font-weight: bold;
            font-size: 14px;
        }

        .stTextArea textarea {
            background-color: #e7f3ff;
            border: 1px solid #d0e6f8;
        }

        /* Tabs styling */
        .stTabs .stTab {
            font-weight: bold;
            color: #2E86C1;
        }

        /* File uploader styling */
        .stFileUploader label {
            font-weight: bold;
            font-size: 14px;
        }

        /* Button styling */
        .stButton button {
            background-color: #2E86C1;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            border-radius: 5px;
            cursor: pointer;
        }

        .stButton button:hover {
            background-color: #1C598A;
        }

        /* Success and error messages */
        .stAlert {
            border-radius: 5px;
            padding: 15px;
        }

        .stSuccess {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .stError {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
