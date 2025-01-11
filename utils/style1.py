def apply_style():
    """Apply custom styles to the Streamlit app."""
    st.markdown(
        """
        <style>
        .stTextInput input, .stTextArea textarea {
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 10px;
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
        .stHeader {
            color: #4CAF50;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
