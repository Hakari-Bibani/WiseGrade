import streamlit as st

def show():
    st.title("Welcome to Code For Impact")
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h2 style="color: #1ABC9C;">Empowering Your Academic Success</h2>
            <p>Navigate through Assignments, Quizzes, and Help to explore more.</p>
        </div>
    """, unsafe_allow_html=True)

    # Add a placeholder for video or image section
    st.markdown("""
        <div class="welcome-section">
            <h3>Start Your Journey Today</h3>
            <div class="video-container">
                <!-- Replace the source with your YouTube link -->
                <iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                </iframe>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Add a sample button for navigation or action
    if st.button("Explore More"):
        st.success("This is where you can add more functionality.")
