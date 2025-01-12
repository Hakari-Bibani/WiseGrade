import random
import string
import traceback
import folium
import pandas as pd

# Set the page style
set_page_style()
@@ -17,6 +19,20 @@ def generate_student_id(name, email):
        return random_numbers + random_letter
    return "N/A"

def find_folium_map(local_context):
    """Search for a Folium map object in the local context."""
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            return var_value
    return None
def find_dataframe(local_context):
    """Search for a Pandas DataFrame or similar in the local context."""
    for var_name, var_value in local_context.items():
        if isinstance(var_value, pd.DataFrame):
            return var_value
    return None
def show():
    st.title("Assignment 1: Mapping Coordinates and Calculating Distances")

@@ -68,22 +84,25 @@ def show():
            local_context = {}
            exec(code_input, {}, local_context)

            # Check for expected outputs (map and summary text)
            if "map_kurdistan" in local_context and "df_distances" in local_context:
                st.success("Code executed successfully!")
                
                # Display the map
                map_object = local_context["map_kurdistan"]
            # Search for outputs
            map_object = find_folium_map(local_context)
            dataframe_object = find_dataframe(local_context)
            # Display outputs
            if map_object:
                st.success("Map generated successfully!")
                map_object.save("map_kurdistan.html")
                st.markdown("### Generated Map")
                st.components.v1.html(map_object._repr_html_(), height=500)
            else:
                st.warning("No Folium map found in the code output.")

                # Display the distance summary
            if dataframe_object is not None:
                st.markdown("### Distance Summary")
                df_distances = local_context["df_distances"]
                st.write(df_distances)
                st.write(dataframe_object)
            else:
                st.warning("Your code executed without errors, but the expected outputs (map and distances) were not found.")
                st.warning("No DataFrame with distances found in the code output.")
        except Exception as e:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())
