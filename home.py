import streamlit as st

def show():
    """Display the Home page content."""
    st.title("Welcome to Code For Impact")
    st.subheader("Empowering students to achieve academic success.")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; padding: 10px; font-size: 1.2em; line-height: 1.5;">
        Welcome to the Code For Impact portal! Here you can access your assignments, quizzes, and additional resources
        designed to support your learning journey. Use the navigation menu on the left to explore the sections.
    </div>
    """, unsafe_allow_html=True)

    # Add a placeholder for future content or videos
    st.markdown("### Featured Content")
    st.markdown("""
    <div class="video-container">
        <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" 
        frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
        </iframe>
    </div>
    """, unsafe_allow_html=True)

    # Example buttons for interaction
    if st.button("Explore Assignments"):
        st.write("Redirecting to Assignments section...")
    if st.button("Explore Quizzes"):
        st.write("Redirecting to Quizzes section...")
