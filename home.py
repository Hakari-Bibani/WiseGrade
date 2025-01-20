import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --primary-color: #2C3E50;
            --secondary-color: #1ABC9C;
            --background-color: linear-gradient(135deg, #ECF0F1, #BDC3C7);
            --text-color: #2C3E50;
        }

        /* Global styles */
        .stApp {
            background: var(--background-color);
            color: var(--text-color);
        }

        /* Welcome section */
        .welcome-section {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #1ABC9C, #16A085);
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .animate-fade-in {
            animation: fadeIn 1.5s ease-in;
        }

        /* Video section */
        .video-section {
            margin: 2rem 0;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .video-container {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 8px;
        }

        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(135deg, #34495E, #2C3E50);
        }

        /* Button styling */
        .stButton>button {
            background-color: var(--secondary-color);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .stButton>button:hover {
            background-color: #16a085;
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)
