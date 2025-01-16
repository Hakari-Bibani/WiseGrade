import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load the Google Sheets credentials from Streamlit secrets
def load_google_sheet():
    try:
        google_sheets_secrets = st.secrets.get("google_sheets", None)
        if not google_sheets_secrets:
            st.error("Google Sheets credentials are missing in Streamlit secrets.")
            return None

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            google_sheets_secrets, scope
        )
        client = gspread.authorize(credentials)

        spreadsheet = client.open_by_key(google_sheets_secrets["spreadsheet_id"])
        return spreadsheet.sheet1

    except Exception as e:
        st.error(f"Error loading Google Sheet: {e}")
        return None

def show():
    st.title("Quiz 1: Google Sheets and Python")

    # Step 1: Validate Student ID
    st.header("Step 1: Enter Your Student ID")
    student_id = st.text_input("Enter Your Student ID")
    verify_button = st.button("Verify Student ID")

    if verify_button:
        worksheet = load_google_sheet()
        if worksheet:
            saved_ids = [row[2] for row in worksheet.get_all_values()[1:]]  # Assuming student_id is in the 3rd column
            if student_id in saved_ids:
                st.success(f"Student ID {student_id} verified. Proceed to the quiz.")
                st.session_state["verified"] = True
            else:
                st.error("Invalid Student ID. Please enter a valid ID from Assignment 2.")
                st.session_state["verified"] = False

    if st.session_state.get("verified", False):
        # Quiz Questions
        st.header("Step 2: Take the Quiz")
        questions = [
            "What is the correct way to access a Google Sheet in Google Colab without using an API?",
            "How can ChatGPT be effectively used to assist in Python programming for processing Google Sheets?",
            "Which of the following steps is required to save processed data back to Google Sheets using the Google Sheets API in Google Colab?",
            "What is the first step to accessing Google Sheets using the Google Sheets API in Google Colab?",
            "How can ChatGPT assist in debugging Python code in your Google Colab workflow?",
            "What is the main advantage of mounting Google Drive in Google Colab for working with Google Sheets?",
            "Your code throws a KeyError when accessing a dictionary. What should you do?",
        ]

        options = [
            [
                "By mounting Google Drive in Colab and accessing the file path directly.",
                "By sharing the Google Sheet link and importing it using a public URL.",
                "By using the gspread library with a service account key.",
                "By exporting the Google Sheet as a CSV file and uploading it to Google Colab.",
            ],
            [
                "ChatGPT automatically integrates with Google Colab to process data.",
                "ChatGPT can write complete working scripts without any user input.",
                "ChatGPT can provide suggestions for improving your code, including optimization and error handling.",
                "ChatGPT replaces the need for learning Python syntax and programming logic.",
            ],
            [
                "Both a and b.",
                "Authenticating Colab with a personal Gmail account using gspread.",
                "Sharing the Google Sheet with a service account email.",
                "Using pandas to write data directly to the Google Sheet without authentication.",
            ],
            [
                "Install the Google Sheets API client library and authenticate with an API key or service account credentials.",
                "Directly import the gspread library without any setup.",
                "Mount Google Drive and access the Google Sheet directly.",
                "Share the Google Sheet link publicly and download the file as a CSV.",
            ],
            [
                "By providing insights into error messages and suggesting corrections or improvements to the code.",
                "By connecting directly to your Colab instance to detect errors.",
                "By automatically fixing errors in real-time as you run the code.",
                "By generating new errors to help understand debugging techniques.",
            ],
            [
                "It provides real-time synchronization between Google Sheets and Colab.",
                "It automatically processes data in Google Sheets without user intervention.",
                "It eliminates the need for authentication using the Google Sheets API.",
                "It allows direct access to all files stored in Google Drive.",
            ],
            [
                "Blame Python for not understanding what you meant.",
                "Check if the key exists in the dictionary and handle the error appropriately.",
                "Write an angry email to Guido van Rossum demanding an explanation.",
                "Take a coffee break and hope the error fixes itself.",
            ],
        ]

        answers = [
            "By sharing the Google Sheet link and importing it using a public URL.",
            "ChatGPT can provide suggestions for improving your code, including optimization and error handling.",
            "Both a and b.",
            "Install the Google Sheets API client library and authenticate with an API key or service account credentials.",
            "By providing insights into error messages and suggesting corrections or improvements to the code.",
            "It provides real-time synchronization between Google Sheets and Colab.",
            "Check if the key exists in the dictionary and handle the error appropriately.",
        ]

        st.write("### Instructions")
        st.write(
            "- Answer all questions before submitting.\n"
            "- Each correct answer is worth 10 points.\n"
            "- Click 'Submit Quiz' when you are ready."
        )

        user_answers = []
        for i, question in enumerate(questions):
            st.subheader(f"Question {i+1}")
            # Set index=0 to pre-select the first option
            answer = st.radio(
                question,
                options[i],
                key=f"q{i+1}",
                index=0
            )
            user_answers.append(answer)

        if st.button("Submit Quiz"):
            score = sum([1 for i in range(len(answers)) if user_answers[i] == answers[i]]) * 10
            st.success(f"You scored {score}/70.")

if __name__ == "__main__":
    show()
