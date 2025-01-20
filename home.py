import streamlit as st

# Import your styling function
from home import apply_custom_styles  # Adjust the import based on your file structure

# Apply custom styles
apply_custom_styles()

# Main app content
def main():
    st.title("Welcome to My Streamlit App")
    st.write("This app demonstrates the use of custom styles in Streamlit.")
    
    # Example sections
    st.markdown("<div class='welcome-section'>Welcome to the polished app!</div>", unsafe_allow_html=True)
    
    st.markdown("## Video Section")
    st.markdown("""
        <div class="video-container">
            <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>
        </div>
    """, unsafe_allow_html=True)

# Call the main function
if __name__ == "__main__":
    main()
