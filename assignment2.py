########################################
# assignment2.py
########################################

import streamlit as st
import traceback
import re
import folium
import pandas as pd

# If you have a style2.py, import your styling function
# from utils.style2 import set_page_style

#############################
# 1. Monkey-Patch Logic
#############################
def preprocess_student_code(code_str):
    """
    1. Remove or un-indent the if __name__ == "__main__": block,
       so that code always executes at the top-level.
    2. Insert lines like `map_object = <var>` or `df_object = <var>`
       after typical variable assignments for a Folium map or DataFrame.
    """
    lines = code_str.split('\n')
    new_lines = []
    skip_block = False
    indent_level_of_main = None

    # --- PART A: Remove the if __name__ == "__main__": guard and un-indent code inside it ---
    for i, line in enumerate(lines):
        # Detect if line has: if __name__ == '__main__':
        if re.search(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', line):
            skip_block = True
            indent_level_of_main = len(line) - len(line.lstrip())
            # Don't add this line
            continue

        if skip_block:
            # We're inside the if __main__ block
            current_indent = len(line) - len(line.lstrip())
            if current_indent > indent_level_of_main:
                # "Un-indent" the line so it always runs
                unindented_line = line.lstrip()
                new_lines.append(unindented_line)
                continue
            else:
                # This line is no longer indented => block ended
                skip_block = False

        if not skip_block:
            new_lines.append(line)

    code_without_main = "\n".join(new_lines)

    # --- PART B: Insert top-level references so the map/df are detectable ---
    final_lines = []
    for line in code_without_main.split('\n'):
        final_lines.append(line)

        # If we see: something = folium.Map(...) or something = create_map(...)
        map_assign_match = re.match(
            r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*folium\.Map.*|.*create_map.*)',
            line
        )
        if map_assign_match:
            var_name = map_assign_match.group(1).strip()
            final_lines.append(f"map_object = {var_name}")

        # If we see: df = pd.DataFrame(...) or df = process_data(...)
        df_assign_match = re.match(
            r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*pd\.DataFrame.*|.*process_data.*|.*read_csv.*)',
            line
        )
        if df_assign_match:
            var_name = df_assign_match.group(1).strip()
            final_lines.append(f"df_object = {var_name}")

    return "\n".join(final_lines)


#############################
# 2. Extended Detection
#############################
def find_folium_map(local_context):
    """
    Try to locate a Folium map by:
    1. Checking for isinstance(var, folium.Map).
    2. Checking for objects that have .save() & ._repr_html_().
    3. Checking for variables named with 'map' that have .save().
    """
    # 1) Direct instance check
    for var_name, var_value in local_context.items():
        if isinstance(var_value, folium.Map):
            return var_value

    # 2) Check for typical Folium methods
    for var_name, var_value in local_context.items():
        if callable(getattr(var_value, "save", None)) and callable(getattr(var_value, "_repr_html_", None)):
            return var_value

    # 3) If var_name contains "map", see if it has a .save() method
    for var_name, var_value in local_context.items():
        if "map" in var_name.lower():
            if hasattr(var_value, "save"):
                return var_value

    return None


def find_dataframe(local_context):
    """
    Attempt to find a DataFrame by:
    1. Checking if any var is a pd.DataFrame.
    2. Checking typical var names (df, data, earthquake_data, etc.).
    3. Checking if it has .head() or .columns (DataFrame-like).
    """
    # 1) Direct instance check
    for var_name, var_value in local_context.items():
        if isinstance(var_value, pd.DataFrame):
            return var_value

    # 2) Typical variable names
    for var_name, var_value in local_context.items():
        if var_name.lower() in ["df", "data", "earthquakes", "earthquake_data"]:
            if hasattr(var_value, "head") and hasattr(var_value, "columns"):
                return var_value

    return None


#############################
# 3. Execute Student Code
#############################
def run_student_code(code_input):
    """
    1. Preprocess the code (remove if __main__ and insert map_object/df_object).
    2. Execute it in a fresh local_context dict.
    3. Attempt to find the Folium map & DataFrame.
    """
    local_context = {}
    try:
        patched_code = preprocess_student_code(code_input)
        exec(patched_code, {}, local_context)
    except Exception as e:
        st.error("An error occurred while executing your code:")
        st.error(traceback.format_exc())
        return None, None

    # Detect map & DataFrame
    map_obj = find_folium_map(local_context)
    df_obj = find_dataframe(local_context)
    return map_obj, df_obj


#############################
# 4. Streamlit UI
#############################
def show():
    # If you have custom styling:
    # set_page_style()

    st.title("Assignment 2: Real-Time Earthquake Data Analysis")

    # Student ID field
    student_id = st.text_input("Enter Your Student ID")

    # Create tabs for assignment details & grading
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])

    with tab1:
        st.markdown("""
        **Objective**  
        In this assignment, you will write a Python script that fetches real-time earthquake data from the USGS Earthquake API, 
        processes the data to filter earthquakes with a magnitude greater than 4.0, 
        and plots the earthquake locations on a map. You will also create a bar chart 
        and a text summary (CSV) of earthquake frequency, magnitude stats, etc.
        
        **Date Range**: January 2nd, 2025 to January 9th, 2025  
        **Libraries**: requests/urllib, pandas, folium, matplotlib/seaborn
        **Expected Output**:
        1. An interactive Folium map (color-coded markers)
        2. A bar chart (frequencies by magnitude range)
        3. A text summary (CSV) of total count, average/max/min magnitude, etc.
        """)

    with tab2:
        st.markdown("""
        **Grading Breakdown**  

        1. **Library Imports (10 Points)**  
        2. **Code Quality (20 Points)**  
        3. **Fetching Data from the API (10 Points)**  
        4. **Filtering Earthquakes (10 Points)**  
        5. **Map Visualization (20 Points)**  
        6. **Bar Chart (15 Points)**  
        7. **Text Summary (15 Points)**  
        8. **Overall Execution (10 Points)**
        """)

    # Code area
    code_input = st.text_area("Paste your code here", height=300)

    # Run & Submit Buttons
    run_button = st.button("Run")
    submit_button = st.button("Submit")

    # RUN logic
    if run_button and code_input:
        map_obj, df_obj = run_student_code(code_input)

        # Display the map
        if map_obj:
            st.success("Map found successfully!")
            st.markdown("### 🗺️ Generated Map")
            st.components.v1.html(map_obj._repr_html_(), height=500)
        else:
            st.warning("No Folium map found in the code output.")

        # Display the DataFrame
        if df_obj is not None:
            st.markdown("### 📊 DataFrame Found")
            st.write(df_obj)
        else:
            st.warning("No DataFrame found in the code output.")

    # SUBMIT logic
    if submit_button and code_input:
        if student_id.strip():
            # If you have a grading function, e.g. grade2.py -> grade_assignment:
            # from grades.grade2 import grade_assignment
            # grade = grade_assignment(code_input)
            # Store to Google Sheet if you like, e.g.:
            # update_google_sheet("", "", student_id, grade, "assignment_2")
            # st.success(f"Submission successful! Your grade: {grade}/100")

            st.success("Submission successful! (Placeholder: Grading logic not implemented in this code.)")
        else:
            st.error("Please enter a valid Student ID before submitting.")


# If you want this file to run standalone, you can do:
# if __name__ == "__main__":
#     import streamlit.web.cli as stcli
#     stcli._main_run_clExplicit("assignment2.py", None)
