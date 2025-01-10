import streamlit as st

def show():
    st.title("Help & Support")
    st.write("Need assistance? Here's how to get help:")
    st.markdown("""
        1. **Check our FAQ section below**  
        2. **Contact your instructor**  
        3. **Submit a support ticket**  
    """)
    st.info("For immediate help, please reach out to your course administrator or instructor.")
