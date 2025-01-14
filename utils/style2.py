# style2.py
def set_page_style():
    """Apply custom styles to the Streamlit app."""
    st.markdown("""
        <style>
            .stApp {
                background-color: #f0f2f6;
                color: #333;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            .stHeader {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
            .stMarkdown {
                font-size: 16px;
                line-height: 1.6;
            }
        </style>
    """, unsafe_allow_html=True)
