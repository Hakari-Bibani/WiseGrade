import streamlit as st
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup
from skimage.metrics import structural_similarity as ssim
from io import StringIO
import grade2
import traceback


def show():
    st.title("Assignment 2: Earthquake Data Analysis")

    # Section 1: Code Input and Analysis
    st.header("Step 1: Analyze Your Code")
    code_input = st.text_area("Paste your Python code here", height=300)

    if st.button("Analyze Code"):
        try:
            analysis_result = grade2.analyze_code(code_input)
            st.success("Code analysis completed!")
            st.json(analysis_result)
        except Exception as e:
            st.error(f"Error during code analysis: {e}")
            st.text(traceback.format_exc())

    # Section 2: Upload Files
    st.header("Step 2: Upload and Validate Outputs")
    uploaded_html = st.file_uploader("Upload HTML Map File", type=["html"])
    uploaded_png = st.file_uploader("Upload PNG Bar Chart", type=["png"])
    uploaded_csv = st.file_uploader("Upload CSV Summary", type=["csv"])

    if st.button("Validate Files"):
        validation_results = {}

        # HTML Validation
        if uploaded_html:
            try:
                html_content = uploaded_html.read()
                validation_results["html"] = grade2.validate_html(html_content)
                st.success("HTML map file validated!")
            except Exception as e:
                validation_results["html"] = {"error": str(e)}
                st.error("Error validating HTML map file.")
        
        # PNG Validation
        if uploaded_png:
            try:
                png_image = Image.open(uploaded_png)
                validation_results["png"] = grade2.validate_png(png_image)
                st.success("PNG bar chart validated!")
            except Exception as e:
                validation_results["png"] = {"error": str(e)}
                st.error("Error validating PNG bar chart.")
        
        # CSV Validation
        if uploaded_csv:
            try:
                csv_data = pd.read_csv(uploaded_csv)
                validation_results["csv"] = grade2.validate_csv(csv_data)
                st.success("CSV summary validated!")
            except Exception as e:
                validation_results["csv"] = {"error": str(e)}
                st.error("Error validating CSV summary.")

        st.json(validation_results)


if __name__ == "__main__":
    show()
