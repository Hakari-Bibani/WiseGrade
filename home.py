import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Animation for moving text */
        @keyframes move {
            0% { transform: translateX(0); }
            50% { transform: translateX(10px); }
            100% { transform: translateX(0); }
        }

        /* Title style */
        .title {
            color: red;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            animation: move 2s infinite;
        }

        /* Video section */
        .video-container {
            text-align: center;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }

        /* Footer text */
        .footer {
            text-align: center;
            font-size: 1.2rem;
            color: #2C3E50;
            margin-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

def show():
    # Apply custom styles
    apply_custom_styles()

    # Title
    st.markdown('<div class="title">Welcome to Code for Impact</div>', unsafe_allow_html=True)

    # Video Section
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    # Replace with your YouTube video link later
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer Text
    st.markdown('<div class="footer">Code for Impact is your partner in academic success</div>', unsafe_allow_html=True)
