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

        /* Title styling */
        .shining-title {
            color: red;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            animation: shine 2s infinite alternate, float 5s infinite ease-in-out;
        }

        /* Animations */
        @keyframes shine {
            0% { text-shadow: 0 0 5px red, 0 0 10px red, 0 0 20px red; }
            100% { text-shadow: 0 0 20px red, 0 0 30px red, 0 0 40px red; }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        /* Video container */
        .video-container {
            margin: 2rem 0;
            text-align: center;
        }

        /* Footer text styling */
        .footer-text {
            margin-top: 2rem;
            text-align: center;
            font-size: 1.2rem;
            color: #34495E;
        }
        </style>
    """, unsafe_allow_html=True)

def show():
    apply_custom_styles()
    
    # Display the title
    st.markdown('<div class="shining-title">Welcome to Code for Impact</div>', unsafe_allow_html=True)

    # Placeholder for the instruction video
    st.markdown("""
        <div class="video-container">
            <iframe width="560" height="315" src="PLACEHOLDER_VIDEO_URL" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen></iframe>
        </div>
    """, unsafe_allow_html=True)

    # Footer text
    st.markdown('<div class="footer-text">Code for Impact is your partner in academic success</div>', unsafe_allow_html=True)
