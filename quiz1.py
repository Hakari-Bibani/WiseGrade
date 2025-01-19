import streamlit as st
from Record.google_sheet import update_google_sheet

# Quiz Questions and Answers
questions = [
    {
        "question": "What is the correct way to access a Google Sheet in Google Colab without using an API?",
        "options": [
            "By mounting Google Drive in Colab and accessing the file path directly.",
            "By sharing the Google Sheet link and importing it using a public URL.",
            "By using the gspread library with a service account key.",
            "By exporting the Google Sheet as a CSV file and uploading it to Google Colab"
        ],
        "answer": "By sharing the Google Sheet link and importing it using a public URL."
    },
    {
        "question": "How can ChatGPT be effectively used to assist in Python programming for processing Google Sheets?",
        "options": [
            "ChatGPT automatically integrates with Google Colab to process data.",
            "ChatGPT can write complete working scripts without any user input.",
            "ChatGPT can provide suggestions for improving your code, including optimization and error handling.",
            "ChatGPT replaces the need for learning Python syntax and programming logic."
        ],
        "answer": "ChatGPT can provide suggestions for improving your code, including optimization and error handling."
    },
    {
        "question": "Which of the following steps is required to save processed data back to Google Sheets using the Google Sheets API in Google Colab?",
        "options": [
            "Authenticating Colab with a personal Gmail account using gspread.",
            "Sharing the Google Sheet with a service account email.",
            "Both a and b.",
            "Using pandas to write data directly to the Google Sheet without authentication."
        ],
        "answer": "Both a and b."
    },
    {
        "question": "What is the first step to accessing Google Sheets using the Google Sheets API in Google Colab?",
        "options": [
            "Install the Google Sheets API client library and authenticate with an API key or service account credentials.",
            "Directly import the gspread library without any setup.",
            "Mount Google Drive and access the Google Sheet directly.",
            "Share the Google Sheet link publicly and download the file as a CSV."
        ],
        "answer": "Install the Google Sheets API client library and authenticate with an API key or service account credentials."
    },
    {
        "question": "How can ChatGPT assist in debugging Python code in your Google Colab workflow?",
        "options": [
            "By providing insights into error messages and suggesting corrections or improvements to the code.",
            "By connecting directly to your Colab instance to detect errors.",
            "By automatically fixing errors in real-time as you run the code.",
            "By generating new errors to help understand debugging techniques."
        ],
        "answer": "By providing insights into error messages and suggesting corrections or improvements to the code."
    },
    {
        "question": "What is the main advantage of mounting Google Drive in Google Colab for working with Google Sheets?",
        "options": [
            "It provides real-time synchronization between Google Sheets and Colab.",
            "It automatically processes data in Google Sheets without user intervention.",
            "It eliminates the need for authentication using the Google Sheets API.",
            "It allows direct access to all files stored in Google Drive."
        ],
        "answer": "It provides real-time synchronization between Google Sheets and Colab."
    },
    {
        "question": "Your code throws a KeyError when accessing a dictionary. What should you do?",
        "options": [
            "Blame Python for not understanding what you meant.",
            "Check if the key exists in the dictionary and handle the error appropriately.",
            "Write an angry email to Guido van Rossum demanding an explanation.",
            "Take a coffee break and hope the error fixes itself."
        ],
        "answer": "Check if the key exists in the dictionary and handle the error appropriately."
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
    st.title("Quiz 1: Python and Google Sheets")

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
            answer = st.radio(
                "Choose an answer:",
                options=["Choose an answer"] + question["options"],
                index=0,
                key=f"question_{i}"
            )
            if answer != "Choose an answer":
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
                    score += 1

            # Update attempts and display score
            st.session_state["attempts"] += 1
            total_score = (score / len(questions)) * 100
            st.success(f"Your score: {total_score}/100")

            # Save grade to Google Sheets
            update_google_sheet(
                full_name="",  # Optional: Add if available
                email="",      # Optional: Add if available
                student_id=student_id,
                grade=total_score,
                current_assignment="quiz_1"
            )

if __name__ == "__main__":
    show()

