import streamlit as st
import folium
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from io import StringIO
import traceback
import sys

def show():
    st.title("Assignment 2: Earthquake Data Analysis")
    st.header("Convert Your Colab Script into Streamlit Application")

    # Section 1: Upload Your Script
    st.markdown("### Step 1: Upload Your Python Script")
    uploaded_file = st.file_uploader("Upload your Python script (.py file)", type=["py"])

    if uploaded_file:
        try:
            # Read uploaded script
            user_code = uploaded_file.read().decode("utf-8")
            st.success("Script uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return

        # Section 2: Extract and Execute Main Points
        st.markdown("### Step 2: Display Main Points from Your Script")

        # Capture script outputs
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            local_context = {}

            # Execute user script
            exec(user_code, {}, local_context)

            # Extract outputs
            folium_map = next(
                (obj for obj in local_context.values() if isinstance(obj, folium.Map)), None
            )
            bar_chart_path = next(
                (obj for obj in local_context.values() if isinstance(obj, str) and obj.endswith(".png")),
                None,
            )
            summary_df = next(
                (obj for obj in local_context.values() if isinstance(obj, pd.DataFrame)), None
            )

            # Display the outputs
            st.markdown("#### 1. HTML Map")
            if folium_map:
                st_folium(folium_map, width=700, height=500)
            else:
                st.warning("No Folium map detected in your script.")

            st.markdown("#### 2. PNG Bar Chart")
            if bar_chart_path:
                st.image(bar_chart_path)
            else:
                st.warning("No PNG bar chart detected in your script.")

            st.markdown("#### 3. Text Summary")
            if summary_df is not None:
                st.dataframe(summary_df)
            else:
                st.warning("No text summary DataFrame detected in your script.")

        except Exception as e:
            st.error(f"An error occurred while processing your script: {e}")
            st.text_area("Traceback", traceback.format_exc(), height=200)
        finally:
            sys.stdout = sys.__stdout__

        # Show captured stdout
        st.markdown("#### Captured Output")
        st.text_area("Output", captured_output.getvalue(), height=200)

    st.markdown("---")
    st.markdown(
        "Ensure that your script includes the following components:\n"
        "1. **Folium Map**: A variable containing a `folium.Map` object.\n"
        "2. **Bar Chart**: Saved as a PNG file.\n"
        "3. **Text Summary**: A `pandas.DataFrame` summarizing the analysis.\n"
    )

if __name__ == "__main__":
    show()
