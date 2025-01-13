# assignment1.py
import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import set_page_style

def show():
    # Apply the custom page style
    set_page_style()

    st.title("Assignment 1: Mapping Coordinates and Calculating Distances")

    # Predefined coordinates for the assignment
    coordinates = {
        "Point 1": (36.325735, 43.928414),
        "Point 2": (36.393432, 44.586781),
        "Point 3": (36.660477, 43.840174),
    }

    # Display the assignment instructions
    with st.expander("Assignment Objective and Requirements"):
        st.markdown(
            """
            ### Objective
            In this assignment, you will write a Python script to:
            1. Plot three geographical coordinates on a map.
            2. Calculate the distances between each pair of points in kilometers.

            ### Task Requirements
            - Add markers for each coordinate.
            - Draw polylines connecting the points.
            - Use popups to display the distances between points.

            ### Coordinates
            - Point 1: Latitude: 36.325735, Longitude: 43.928414
            - Point 2: Latitude: 36.393432, Longitude: 44.586781
            - Point 3: Latitude: 36.660477, Longitude: 43.840174

            Use Python libraries like `folium`, `geopy`, and `pandas` for the task.
            """
        )

    # Student script input area
    st.markdown("### Submit Your Python Code Below")
    code_input = st.text_area("Paste your Python script here", height=200)

    # Run and visualize the script
    if st.button("Run Script"):
        if not code_input.strip():
            st.warning("Please paste your Python script to run.")
        else:
            try:
                # Create a local execution context for the student's code
                local_context = {}
                exec(code_input, {}, local_context)

                # Extract folium map if present
                map_object = None
                for var in local_context.values():
                    if isinstance(var, folium.Map):
                        map_object = var
                        break

                if map_object:
                    st.success("Map generated successfully!")
                    st_folium(map_object, width=700, height=500)
                else:
                    st.warning("No folium map was found in the code output.")

                # Extract DataFrame for distances if present
                dataframe = None
                for var in local_context.values():
                    if isinstance(var, pd.DataFrame):
                        dataframe = var
                        break

                if dataframe is not None:
                    st.markdown("### Distance Calculations")
                    st.dataframe(dataframe)
                else:
                    st.warning("No DataFrame found displaying distances.")

            except Exception as e:
                st.error("An error occurred while running your script:")
                st.error(str(e))
