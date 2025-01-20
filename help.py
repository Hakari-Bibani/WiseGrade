import streamlit as st

def show():
    # Page Title
    st.title("Help & Support")
    
    # Introduction Section
    st.write("If you need assistance, we're here to help. Please check the options below to find a solution to your problem.")

    # Instructions Section
    st.markdown(
        """
        ### How to Get Help:
        1. **Check the FAQ section below** for quick answers to common questions.
        2. **Contact your instructor** for further assistance.
        """
    )

    # FAQ Section
    st.markdown("### Frequently Asked Questions (FAQ)")

    with st.expander("Can I resubmit assignments?"):
        st.write("Yes, you can resubmit assignments until the deadline for the next assignment. After that, resubmissions for previous assignments will no longer be accepted.")

    with st.expander("Can I resubmit quizzes?"):
        st.write("No, quizzes can only be submitted once.")

    with st.expander("Should I save my student ID?"):
        st.write("Yes, you should save your student ID. It will be required to access assignments.")

    with st.expander("What if I forget my student ID?"):
        st.write("If you forget your student ID, please email [meermiro299@gmail.com](mailto:meermiro299@gmail.com) to request it.")

    # Contact Section
    st.markdown(
        """
        ### Need More Help?
        If you have any further questions or concerns, feel free to reach out to us via email at [meermiro299@gmail.com](mailto:meermiro299@gmail.com).
        """
    )

# Call the show function to display the interface
if __name__ == "__main__":
    show()
