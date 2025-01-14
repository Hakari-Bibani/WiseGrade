import streamlit as st
import traceback
import sys
from io import StringIO

def convert_colab_to_streamlit(script_code):
    """
    Converts a Google Colab script into a Streamlit-compatible script.
    """
    # Define replacements for key components
    replacements = {
        # Replace folium.Map with Streamlit rendering
        "map_object.save(": "st.components.v1.html(",
        # Replace matplotlib/seaborn chart saving with Streamlit rendering
        "plt.savefig(": "st.pyplot(",
        # Replace pandas DataFrame display with Streamlit display
        "print(df)": "st.dataframe(df)",
    }

    # Apply replacements dynamically
    for old, new in replacements.items():
        script_code = script_code.replace(old, new)

    return script_code


def show():
    st.title("Assignment 2: Convert and Display Colab Script in Streamlit")

    # Upload the Colab script
    uploaded_script = st.file_uploader("Upload your Python script (.py)", type="py")

    if uploaded_script:
        # Read and display the original script
        original_script = uploaded_script.read().decode("utf-8")
        st.subheader("Original Colab Script")
        st.code(original_script, language="python")

        # Convert the script to Streamlit-compatible format
        try:
            modified_script = convert_colab_to_streamlit(original_script)
            st.subheader("Modified Streamlit-Compatible Script")
            st.code(modified_script, language="python")

            # Capture stdout
            old_stdout = sys.stdout
            new_stdout = StringIO()
            sys.stdout = new_stdout

            # Execute the modified script
            local_context = {}
            exec(modified_script, {}, local_context)

            # Display the captured outputs
            st.subheader("Captured Outputs")
            st.text(new_stdout.getvalue())

        except Exception as e:
            st.error(f"An error occurred while processing the script: {e}")
            st.text(traceback.format_exc())

        finally:
            # Restore stdout
            sys.stdout = old_stdout


if __name__ == "__main__":
    show()
