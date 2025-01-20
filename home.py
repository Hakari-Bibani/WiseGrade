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
            margin-bottom: 1rem; /* Reduced space below the title */
        }
        </style>
    """, unsafe_allow_html=True)

def show():
    # Apply custom styles
    apply_custom_styles()

    # Title
    st.markdown('<div class="title">Welcome to Code for Impact</div>', unsafe_allow_html=True)

    # Video Section
    # Replace the placeholder URL with the real YouTube video link
    video_url = "https://www.youtube.com/watch?v=YOUR_REAL_VIDEO_LINK"
    st.video(video_url)
