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
        ".save(": "._repr_html_()",
        "folium.Map": "st.components.v1.html",
        # Replace matplotlib/seaborn chart saving with Streamlit rendering
        "plt.savefig(": "st.pyplot(",
        # Replace pandas DataFrame display with Streamlit display
        "print(": "st.text(",
        "display(": "st.dataframe(",
    }

    # Apply replacements dynamically
    for old, new in replacements.items():
        script_code = script_code.replace(old, new)

    return script_code


def show():
    st.title("Assignment 2: Convert and Display Colab Code in Streamlit")

    # Step 1: Paste Code
    st.header("Step 1: Paste Your Code Below")
    pasted_code = st.text_area(
        "Paste your Python script here",
        height=300,
        placeholder="Paste your Google Colab script here...",
    )

    if pasted_code:
        # Display the original script
        st.subheader("Original Colab Script")
        st.code(pasted_code, language="python")

        # Convert the script to Streamlit-compatible format
        try:
            modified_script = convert_colab_to_streamlit(pasted_code)
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
            captured_output = new_stdout.getvalue()
            if captured_output:
                st.text(captured_output)

            # Display folium map
            map_object = next(
                (obj for obj in local_context.values() if "folium.Map" in str(type(obj))),
                None,
            )
            if map_object:
                st.subheader("Interactive Map")
                map_html = map_object._repr_html_()
                st.components.v1.html(map_html, height=500)

            # Display matplotlib figure
            plt_figure = next(
                (obj for obj in local_context.values() if "matplotlib.figure" in str(type(obj))),
                None,
            )
            if plt_figure:
                st.subheader("Bar Chart")
                st.pyplot(plt_figure)

            # Display pandas DataFrame
            dataframe_object = next(
                (obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)),
                None,
            )
            if dataframe_object is not None:
                st.subheader("Text Summary")
                st.dataframe(dataframe_object)

        except Exception as e:
            st.error("An error occurred while processing the code:")
            st.text(traceback.format_exc())

        finally:
            # Restore stdout
            sys.stdout = old_stdout


if __name__ == "__main__":
    show()
