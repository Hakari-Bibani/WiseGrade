import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from io import BytesIO
import base64
import traceback
import sys
import matplotlib.pyplot as plt


def display_html_map(map_html_file):
    """
    Reads an HTML file containing a Folium map and displays it in Streamlit.
    """
    try:
        with open(map_html_file, 'r') as f:
            map_html = f.read()
        st.components.v1.html(map_html, width=800, height=500)
    except Exception as e:
        st.error(f"Error displaying map: {e}")


def display_bar_chart_as_image(chart_file):
    """
    Reads a PNG bar chart file and displays it in Streamlit.
    """
    try:
        with open(chart_file, "rb") as f:
            chart_data = f.read()
        st.image(chart_data, caption="Bar Chart", use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying bar chart: {e}")


def show():
    st.title("Assignment 2: Display Outputs")
    
    st.header("Step 1: Upload Your Outputs")
    map_file = st.file_uploader("Upload your map (HTML file):", type=["html"])
    chart_file = st.file_uploader("Upload your bar chart (PNG file):", type=["png"])
    summary_file = st.file_uploader("Upload your summary (CSV file):", type=["csv"])

    if st.button("Display Outputs"):
        if map_file:
            st.subheader("Interactive Map")
            map_path = f"/tmp/{map_file.name}"
            with open(map_path, "wb") as f:
                f.write(map_file.getbuffer())
            display_html_map(map_path)
        else:
            st.warning("No map uploaded.")

        if chart_file:
            st.subheader("Bar Chart")
            display_bar_chart_as_image(chart_file)
        else:
            st.warning("No bar chart uploaded.")

        if summary_file:
            st.subheader("Summary Data")
            try:
                summary_df = pd.read_csv(summary_file)
                st.dataframe(summary_df)
            except Exception as e:
                st.error(f"Error reading summary file: {e}")
        else:
            st.warning("No summary uploaded.")


if __name__ == "__main__":
    show()
