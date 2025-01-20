import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Styling for the title */
        .title {
            color: red;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            animation: moveTitle 2s infinite alternate;
        }

        /* Styling for the subtitle */
        .subtitle {
            color: #2C3E50;
            font-size: 1.5rem;
            text-align: center;
            margin-top: 1rem;
        }

        /* Styling for the footer text */
        .footer-text {
            color: #2C3E50;
            font-size: 1rem;
            text-align: center;
            margin-top: 2rem;
        }

        /* Animation for the title */
        @keyframes moveTitle {
            from {
                transform: translateY(0);
            }
            to {
                transform: translateY(10px);
            }
        }

        /* Video placeholder styling */
        .video-placeholder {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 2rem auto;
            padding: 1rem;
            width: 80%;
            height: 250px;
            background-color: #ECF0F1;
            border: 2px dashed #BDC3C7;
            color: #7F8C8D;
            font-size: 1.2rem;
            border-radius: 8px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

def show():
    apply_custom_styles()

    # Title with animation
    st.markdown('<div class="title">Welcome to Code for Impact</div>', unsafe_allow_html=True)

    # Subtitle
    st.markdown('<div class="subtitle">Impact is your partner in academic success</div>', unsafe_allow_html=True)

    # Video placeholder
    st.markdown('<div class="video-placeholder">Instructional Video Placeholder</div>', unsafe_allow_html=True)

    # Footer text
    st.markdown('<div class="footer-text">Code for Impact is your partner in academic success</div>', unsafe_allow_html=True)
