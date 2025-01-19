import streamlit as st
from Record.google_sheet import update_google_sheet

# Quiz Questions and Points
questions = [
    {
        "question": "Splitting a script into multiple smaller scripts helps make the code more manageable and easier to debug.",
        "points": 35,
        "answer": True
    },
    {
        "question": "The main.py script is responsible for importing and executing functions or modules stored in other scripts saved on Google Drive.",
        "points": 35,
        "answer": True
    },
    {
        "question": "Saving smaller scripts in Google Drive and importing them into Google Colab increases the risk of altering the main script when making changes.",
        "points": 30,
        "answer": False
    }
]

# Maximum number of submissions allowed
MAX_ATTEMPTS = 3

# Validate Student ID
def validate_student_id(student_id):
    try:
        # Replace with actual logic to verify Student ID from Google Sheet
        # Assuming IDs are stored in the third column of a sheet
        google_sheets_secrets = st.secrets.get("google_sheets", None)
        if not google_sheets_secrets:
            st.error("Google Sheets credentials are missing in Streamlit secrets.")
            return False

        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_secrets, scope)
        client = gspread.authorize(credentials)

        spreadsheet = client.open_by_key(google_sheets_secrets["spreadsheet_id"])
        worksheet = spreadsheet.sheet1
        saved_ids = [row[2] for row in worksheet.get_all_values()[1:]]  # Assuming Student ID in 3rd column

        return student_id in saved_ids

    except Exception as e:
        st.error(f"Error validating Student ID: {e}")
        return False

def show():
    st.title("Quiz 2: Python and Script Management")

    # Step 1: Enter Student ID
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Enter Your Student ID")
    verify_button = st.button("Verify Student ID")

    if "attempts" not in st.session_state:
        st.session_state["attempts"] = 0

    if verify_button:
        if validate_student_id(student_id):
            st.success("Student ID validated. You can proceed with the quiz.")
            st.session_state["validated"] = True
        else:
            st.error("Invalid Student ID. Please use the ID associated with Assignment 1.")
            st.session_state["validated"] = False

    if st.session_state.get("validated", False):
        st.header("Step 2: Answer the Questions")

        # Initialize user answers
        if "user_answers" not in st.session_state:
            st.session_state["user_answers"] = [None] * len(questions)

        # Quiz questions
        for i, question in enumerate(questions):
            st.write(f"**Q{i+1}: {question['question']}**")
            answer = st.checkbox(
                "Select True or False:",
                value=False,  # Default to False
                key=f"question_{i}"
            )
            st.session_state["user_answers"][i] = answer

        # Submit Button
        submit_button = st.button("Submit Quiz")

        if submit_button:
            if st.session_state["attempts"] >= MAX_ATTEMPTS:
                st.error("You have reached the maximum number of attempts for this quiz.")
                return

            # Check if all questions are answered
            if None in st.session_state["user_answers"]:
                st.error("Please answer all the questions before submitting.")
                return

            # Calculate Score
            score = 0
            for i, question in enumerate(questions):
                if st.session_state["user_answers"][i] == question["answer"]:
                    score += question["points"]

            # Update attempts and display score
            st.session_state["attempts"] += 1
            total_score = score
            st.success(f"Your score: {total_score}/100")

            # Save grade to Google Sheets
            update_google_sheet(
                full_name="",  # Optional: Add if available
                email="",      # Optional: Add if available
                student_id=student_id,
                grade=total_score,
                current_assignment="quiz_2"
            )

if __name__ == "__main__":
    show()
