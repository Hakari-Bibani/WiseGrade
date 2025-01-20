import streamlit as st
from Record.google_sheet import update_google_sheet

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

# Rest of the code remains the same as in the previous response, including:
# - MAX_ATTEMPTS
# - add_custom_css()
# - validate_student_id()
# - show()
# - All the styling and functionality

MAX_ATTEMPTS = 3

def add_custom_css():
    st.markdown("""
        <style>
        /* Main container */
        .main {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Modern card design */
        .quiz-card {
            background-color: white;
            border-radius: 12px;
            padding: 24px;
            margin: 16px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid #f0f0f0;
            transition: all 0.3s ease;
        }
        
        .quiz-card:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transform: translateY(-1px);
        }
        
        /* Question styling */
        .question-header {
            display: flex;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #f3f4f6;
        }
        
        .question-number {
            background-color: #f3f4f6;
            color: #4b5563;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.9em;
            font-weight: 500;
            margin-right: 12px;
        }
        
        .question-text {
            font-size: 1.1em;
            color: #1f2937;
            font-weight: 500;
            line-height: 1.5;
            margin-bottom: 20px;
        }
        
        /* Radio button styling */
        .stRadio > div {
            background-color: #f8fafc;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
        }
        
        .stRadio > div > div {
            gap: 16px;
        }
        
        .stRadio > div > div > label {
            background-color: white;
            padding: 12px 16px;
            border-radius: 8px;
            border: 2px solid #e5e7eb;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .stRadio > div > div > label:hover {
            border-color: #3b82f6;
            transform: translateY(-1px);
        }
        
        /* Student ID input styling */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #e5e7eb;
            padding: 12px 16px;
            font-size: 1em;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Button styling */
        .stButton > button {
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Progress bar */
        .progress-bar {
            background-color: #f3f4f6;
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }
        
        /* Results section */
        .results-card {
            background-color: #f8fafc;
            border-radius: 12px;
            padding: 24px;
            margin-top: 24px;
        }
        
        /* Hide default streamlit elements */
        #MainMenu, footer {display: none;}
        
        /* Option container styling */
        .option-container {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            padding: 12px 16px;
            margin: 8px 0;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .option-container:hover {
            border-color: #3b82f6;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Selected option styling */
        .option-selected {
            background-color: #f0f9ff;
            border-color: #3b82f6;
        }
        </style>
    """, unsafe_allow_html=True)

def validate_student_id(student_id):
    try:
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
        saved_ids = [row[2] for row in worksheet.get_all_values()[1:]]

        return student_id in saved_ids

    except Exception as e:
        st.error(f"Error validating Student ID: {e}")
        return False

def show():
    add_custom_css()
    
    st.title("📚 Quiz 1: Python and Google Sheets")
    
    # Student ID Section
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            student_id = st.text_input("🆔 Enter Your Student ID", key="student_id_input")
        with col2:
            verify_button = st.button("Verify ID", type="primary", use_container_width=True)

    if "attempts" not in st.session_state:
        st.session_state["attempts"] = 0

    if verify_button:
        if validate_student_id(student_id):
            st.success("✅ ID Verified - You may proceed with the quiz")
            st.session_state["validated"] = True
        else:
            st.error("❌ Invalid ID - Please use your Assignment 1 ID")
            st.session_state["validated"] = False

    if st.session_state.get("validated", False):
        if "user_answers" not in st.session_state:
            st.session_state["user_answers"] = [None] * len(questions)

        # Progress tracking
        answered = sum(1 for ans in st.session_state["user_answers"] if ans is not None)
        st.markdown(f"""
            <div class="progress-bar">
                📝 Progress: {answered}/{len(questions)} questions answered
            </div>
        """, unsafe_allow_html=True)

        # Quiz Questions
        for i, question in enumerate(questions):
            with st.container():
                st.markdown(f"""
                    <div class="quiz-card">
                        <div class="question-header">
                            <div class="question-number">Question {i+1}</div>
                            <div class="question-text">{question['question']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                answer = st.radio(
                    "",
                    options=question["options"],
                    key=f"question_{i}",
                    label_visibility="collapsed"
                )
                
                if answer:
                    st.session_state["user_answers"][i] = answer

        # Submit section
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.button(
                "📤 Submit Quiz",
                type="primary",
                use_container_width=True
            )

        if submit_button:
            if st.session_state["attempts"] >= MAX_ATTEMPTS:
                st.error("❌ Maximum attempts reached")
                return

            if None in st.session_state["user_answers"]:
                st.error("❌ Please answer all questions before submitting")
                return

            score = sum(1 for i, q in enumerate(questions) 
                       if st.session_state["user_answers"][i] == q["answer"])
            
            total_score = (score / len(questions)) * 100
            st.session_state["attempts"] += 1
            
            # Show results
            st.markdown("### 📊 Quiz Results")
            st.progress(total_score/100)
            st.success(f"Your score: {total_score:.1f}/100")
            
            # Save to Google Sheets
            update_google_sheet(
                full_name="",
                email="",
                student_id=student_id,
                grade=total_score,
                current_assignment="quiz_1"
            )

if __name__ == "__main__":
    show()
