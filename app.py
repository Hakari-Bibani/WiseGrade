import streamlit as st
from streamlit_option_menu import option_menu
import home
import style
import importlib

# Apply custom styles from style.py
style.apply_custom_styles()

# Sidebar Navigation
with st.sidebar:
    st.title("GradeWise")

    # Dynamic Navigation Menu
    menu_options = {
        "Home": "home",
        "Assignments": {
            f"Assignment {i}": f"assignment{i}" for i in range(1, 5)
        },
        "Quizzes": {
            f"Quiz {i}": f"quiz{i}" for i in range(1, 5)
        },
        "Help": "help"
    }

    # Render main options
    selected = option_menu(
        menu_title=None,
        options=list(menu_options.keys()),
        icons=["house", "book", "pencil-square", "question-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )

    # Initialize sub-selection state for Assignments and Quizzes
    sub_selected = None
    if selected in ["Assignments", "Quizzes"]:
        # Add a placeholder option to avoid default selection
        options = ["Select"] + list(menu_options[selected].keys())
        sub_selected = st.selectbox(
            f"Select a {selected[:-1]}",
            options,
            key=f"{selected}_selection",
        )
        if sub_selected != "Select":
            selected = menu_options[selected][sub_selected]
        else:
            selected = "home"  # Stay on Home if no valid sub-option is selected
    else:
        selected = menu_options[selected]

# Debugging: Print the resolved module name
st.write(f"Selected module: {selected}")  # For debugging, can be removed later

# Main content area
try:
    if selected == "home":
        home.show()  # Display the Home page
    else:
        # Dynamically import the selected module
        module = importlib.import_module(selected)
        if hasattr(module, "show"):
            module.show()  # Call the show function
        else:
            st.error(f"The module '{selected}' does not have a valid entry point.")
except ImportError:
    st.error(f"Module '{selected}' not found. Please check your file names or paths.")

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; font-size: 0.9em; color: #666;">
        GradeWise © 2024 - Your Partner in Academic Success
    </div>
""", unsafe_allow_html=True)
