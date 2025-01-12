import streamlit as st
import traceback
import io
import os
import sys
import shutil

# The libraries we want to patch
import folium
import matplotlib.pyplot as plt

from utils.style2 import set_page_style
from grades.grade2 import grade_assignment
from Record.google_sheet import update_google_sheet

def show():
    set_page_style()
    st.title("Assignment 2: Real-Time Earthquake Data Analysis")

    # 1) Student ID
    student_id = st.text_input("Enter Your Student ID")

    # 2) Tabs for assignment details
    tab1, tab2 = st.tabs(["Assignment Details", "Grading Details"])
    with tab1:
        st.markdown("... (Your assignment instructions) ...")
    with tab2:
        st.markdown("... (Your grading details) ...")

    # 3) Code text area
    code_input = st.text_area("Paste your code below:", height=300)

    # 4) Buttons
    run_button = st.button("Run")
    submit_button = st.button("Submit")

    # ---------------------------------------------------------
    #  MONKEY-PATCH SECTION
    # ---------------------------------------------------------

    # (A) Patch 'print' to capture all printed output in a buffer
    printed_buffer = io.StringIO()
    orig_print = print  # keep original Python print

    def patched_print(*args, **kwargs):
        text_str = " ".join(str(a) for a in args) + "\n"
        printed_buffer.write(text_str)
        # Still call original print so we can see it in logs (optional)
        orig_print(*args, **kwargs)

    # Override built-in print globally
    import builtins
    builtins.print = patched_print

    # (B) Patch folium.Map.save to always also copy to "earthquake_map.html"
    orig_folium_save = folium.Map.save

    def custom_folium_save(self, outfile, *args, **kwargs):
        # Call original save method
        orig_folium_save(self, outfile, *args, **kwargs)
        # Copy user’s chosen file to "earthquake_map.html" (overwrite if needed)
        if outfile != "earthquake_map.html":
            shutil.copyfile(outfile, "earthquake_map.html")

    folium.Map.save = custom_folium_save

    # (C) Patch matplotlib.pyplot.savefig to also copy to "earthquake_frequency.png"
    orig_plt_savefig = plt.savefig

    def custom_plt_savefig(fname, *args, **kwargs):
        orig_plt_savefig(fname, *args, **kwargs)
        if fname != "earthquake_frequency.png":
            shutil.copyfile(fname, "earthquake_frequency.png")

    plt.savefig = custom_plt_savefig

    # ---------------------------------------------------------
    # RUN THE USER CODE
    # ---------------------------------------------------------

    if run_button and code_input:
        # Cleanup any old files from previous runs
        if os.path.exists("earthquake_map.html"):
            os.remove("earthquake_map.html")
        if os.path.exists("earthquake_frequency.png"):
            os.remove("earthquake_frequency.png")

        # Also clear the printed_buffer
        printed_buffer.truncate(0)
        printed_buffer.seek(0)

        # Safely run user code
        try:
            local_context = {}
            exec(code_input, {}, local_context)
        except Exception:
            st.error("An error occurred while executing your code:")
            st.error(traceback.format_exc())

        # Retrieve all captured prints
        printed_output = printed_buffer.getvalue()

        # 1) Display any printed output
        if printed_output.strip():
            st.markdown("### Printed Summary")
            st.text(printed_output)
        else:
            st.warning("No text summary found in the output.")

        # 2) Display the Folium map
        if os.path.exists("earthquake_map.html"):
            st.markdown("### Generated Earthquake Map")
            with open("earthquake_map.html", "r", encoding="utf-8") as f:
                html_map = f.read()
            st.components.v1.html(html_map, height=600)
        else:
            st.warning("No map file (earthquake_map.html) found.")

        # 3) Display the bar chart
        if os.path.exists("earthquake_frequency.png"):
            st.markdown("### Generated Bar Chart")
            st.image("earthquake_frequency.png")
        else:
            st.warning("No bar chart file (earthquake_frequency.png) found.")

        # Restore the original print (optional cleanup)
        builtins.print = orig_print
        folium.Map.save = orig_folium_save
        plt.savefig = orig_plt_savefig

    # ---------------------------------------------------------
    # SUBMIT
    # ---------------------------------------------------------
    if submit_button and code_input:
        if student_id:
            grade = grade_assignment(code_input)
            update_google_sheet("", "", student_id, grade, "assignment_2")
            st.success(f"Submission successful! Your grade: {grade}/100")
        else:
            st.error("Please enter a valid Student ID before submitting.")
