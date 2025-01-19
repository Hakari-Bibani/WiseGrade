import streamlit as st

def show():
    # Welcome section with animation
    st.markdown("""
        <div class="welcome-section">
            <h1 class="animate-fade-in">Welcome to Code For Impact</h1>
            <h3 class="animate-fade-in">Your Partner in Academic Success!</h3>
        </div>
    """, unsafe_allow_html=True)

    # Tutorial video section
    st.markdown("""
        <div class="video-section">
            <h2>Quick Start Guide</h2>
            <div class="video-container">
                <iframe
                    src="https://www.youtube.com/embed/YOUR_VIDEO_ID?autoplay=1&mute=1"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                ></iframe>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Quick stats and info
    st.markdown("<div class='stats-section'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Available Assignments", "4")
    with col2:
        st.metric("Available Quizzes", "4")
    with col3:
        st.metric("Active Students", "100+")
    st.markdown("</div>", unsafe_allow_html=True)

