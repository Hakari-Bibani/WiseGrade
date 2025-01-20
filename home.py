import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Title styling with animation */
        .title {
            color: red;
            font-size: 3rem;
            text-align: center;
            animation: slide 2s infinite alternate;
        }

        @keyframes slide {
            from { transform: translateX(0); }
            to { transform: translateX(10px); }
        }

        /* Placeholder for video */
        .video-placeholder {
            width: 100%;
            height: 315px; /* Matches YouTube video aspect ratio */
            background-color: black;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 1.2rem;
        }

        /* Footer text styling */
        .footer-text {
            text-align: center;
            font-size: 1.5rem;
            margin-top: 2rem;
            color: #2C3E50;
        }
        </style>
    """, unsafe_allow_html=True)

def show():
    apply_custom_styles()
    
    # Display the animated title
    st.markdown('<div class="title">Welcome to Code for Impact</div>', unsafe_allow_html=True)
    
    # Add some spacing
    st.write("")
    st.write("")
    
    # Display the video placeholder
    st.markdown('<div class="video-placeholder">[ Video Placeholder ]</div>', unsafe_allow_html=True)
    
    # Add the footer text
    st.markdown('<div class="footer-text">Code for Impact is your partner in academic success</div>', unsafe_allow_html=True)
