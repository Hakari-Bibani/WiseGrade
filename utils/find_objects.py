import folium
import pandas as pd

def find_folium_map(local_context):
    """
    Attempt to locate a Folium map by:
    1. Checking if any var is an instance of folium.Map.
    2. Checking if a var has a 'save' or '_repr_html_' method.
    3. Checking if var name contains 'map'.
    """
    # First pass: direct instance check
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            return var_value

    # Second pass: check method signatures
    for var_name, var_value in local_context.items():
        if callable(getattr(var_value, "save", None)) and callable(getattr(var_value, "_repr_html_", None)):
            return var_value

    # Third pass: check for var_name containing 'map'
    for var_name, var_value in local_context.items():
        if "map" in var_name.lower():
            # quick check if it has "save" method
            if hasattr(var_value, "save"):
                return var_value

    return None

def find_dataframe(local_context):
    """
    Attempt to find a DataFrame by:
    1. Checking if any var is an instance of pd.DataFrame.
    2. Checking typical var names that might hold a DF (like 'df', 'data', 'earthquakes', etc.).
    3. Checking if the object has DataFrame-like attributes (.head(), .columns).
    """
    # Direct instance check
    for var_name, var_value in local_context.items():
        if isinstance(var_value, pd.DataFrame):
            return var_value

    # Second pass: check typical var names
    for var_name, var_value in local_context.items():
        if var_name.lower() in ["df", "data", "earthquakes", "earthquake_data"]:
            if hasattr(var_value, "head") and hasattr(var_value, "columns"):
                return var_value

    return None
