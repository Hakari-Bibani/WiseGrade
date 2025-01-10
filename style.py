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

        .animate-fade-in {
            animation: fadeIn 1.5s ease-in;
        }

        /* Video section */
        .video-section {
            margin: 2rem 0;
            padding: 1rem;
        }

        .video-container {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            max-width: 100%;
        }

        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
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

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

