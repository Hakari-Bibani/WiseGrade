if submit_button:
    try:
        # Validate uploads
        if uploaded_html is None:
            st.error("Please upload an HTML file.")
            return
        if uploaded_excel is None:
            st.error("Please upload your Excel file.")
            return

        # Save the uploaded files temporarily
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)

        # Save HTML file
        html_path = os.path.join(temp_dir, "uploaded_map.html")
        with open(html_path, "wb") as f:
            f.write(uploaded_html.getvalue())

        # Save Excel file
        excel_path = os.path.join(temp_dir, "uploaded_sheet.xlsx")
        with open(excel_path, "wb") as f:
            f.write(uploaded_excel.getvalue())

        # Path to the correct Excel file
        correct_excel_path = "grades/correct_assignment3.xlsx"
        if not os.path.exists(correct_excel_path):
            st.error("The correct reference Excel file is missing. Contact your instructor.")
            return

        # Grade the assignment
        scores = grade_assignment(code_input, html_path, excel_path, correct_excel_path)

        # Display detailed feedback
        st.header("Grading Feedback")
        for category, score in scores.items():
            st.write(f"**{category}:** {score} / 100" if category == "Total" else f"**{category}:** {score} points")

        # Prevent resubmission
        st.session_state["assignment3_submitted"] = True

    except Exception as e:
        st.error(f"An error occurred during submission: {e}")
