import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --primary-color: #2C3E50;
            --secondary-color: #1ABC9C;
            --background-color: #ECF0F1;
            --text-color: #2C3E50;
        }

        /* Global styles */
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }

        /* Welcome section */
        .welcome-section {
            text-align: center;
            padding: 2rem 0;
        }

        /* Animated red title */
        .animated-title {
            color: red;
            font-size: 2.5rem;
            font-weight: bold;
            animation: slideIn 2s infinite alternate;
        }

        @keyframes slideIn {
            0% { transform: translateX(0); }
            100% { transform: translateX(10px); }
        }

        /* Video section */
        .video-section {
            margin: 2rem 0;
            padding: 1rem;
        }

        /* Sidebar styling */
        .css-1d391kg {
            background-color: var(--primary-color);
        }

        /* Button styling */
        .stButton>button {
            background-color: var(--secondary-color);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #16a085;
            transform: translateY(-2px);
        }

        </style>
    """, unsafe_allow_html=True)

def show():
    apply_custom_styles()  # Apply the custom styles
    
    # Home page content
    st.markdown("<div class='welcome-section'>", unsafe_allow_html=True)
    st.markdown("<div class='animated-title'>Welcome to Code For Impact</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Placeholder for video link
    st.markdown("<div class='video-section'>", unsafe_allow_html=True)
    st.write("Watch the demo video about our platform [here](https://example.com).")  # Replace with your link
    st.markdown("</div>", unsafe_allow_html=True)
