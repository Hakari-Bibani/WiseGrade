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

MAX_ATTEMPTS = 1

def add_custom_css():
    st.markdown("""
        <style>
        /* Modern container styling */
        .question-container {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 24px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #f0f0f0;
        }
        
        /* Question text styling */
        .question-text {
            font-size: 1.1em;
            color: #1f1f1f;
            line-height: 1.5;
            margin-bottom: 20px;
        }
        
        /* Custom radio button styling */
        .stRadio > div {
            display: flex;
            gap: 12px;
        }
        
        .stRadio > div > label {
            flex: 1;
            background-color: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 12px 24px;
            text-align: center;
            transition: all 0.2s ease;
            cursor: pointer;
            font-weight: 500;
            color: #495057;
            min-width: 120px;
        }
        
        .stRadio > div > label:hover {
            background-color: #e9ecef;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        /* Hide default radio button */
        .stRadio input {
            position: absolute;
            opacity: 0;
            cursor: pointer;
        }
        
        /* Selected state styling */
        .stRadio > div > label[data-checked="true"] {
            background-color: #0066cc;
            color: white;
            border-color: #0066cc;
        }
        
        /* Remove default streamlit label */
        .stRadio > label {
            display: none !important;
        }
        
        /* Hide default help text icon */
        .stRadio > div > div > span {
            display: none !important;
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
    
    st.title("Quiz 2: Python and Script Management")
    
    # Step 1: Enter Student ID
    with st.container():
        st.header("Step 1: Enter Your Student ID")
        col1, col2 = st.columns([3, 1])
        with col1:
            student_id = st.text_input("Enter Your Student ID")
        with col2:
            verify_button = st.button("Verify ID")

    if "attempts" not in st.session_state:
        st.session_state["attempts"] = 0

    if verify_button:
        if validate_student_id(student_id):
            st.success("✅ Student ID validated. You can proceed with the quiz.")
            st.session_state["validated"] = True
        else:
            st.error("❌ Invalid Student ID. Please use the ID associated with Assignment 1.")
            st.session_state["validated"] = False

    if st.session_state.get("validated", False):
        st.header("Step 2: Answer the Questions")

        if "user_answers" not in st.session_state:
            st.session_state["user_answers"] = [None] * len(questions)

        # Quiz questions with improved UI
        for i, question in enumerate(questions):
            with st.container():
                st.markdown(f"""
                    <div class="question-container">
                        <div class="question-text">
                            Q{i+1}: {question['question']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                answer = st.radio(
                    "",  # Empty label
                    options=["True", "False"],
                    key=f"question_{i}",
                    horizontal=True,
                    label_visibility="collapsed"
                )
                st.session_state["user_answers"][i] = answer == "True"

        # Submit Button with improved styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.button(
                "Submit Quiz",
                type="primary",
                use_container_width=True,
            )

        if submit_button:
            if st.session_state["attempts"] >= MAX_ATTEMPTS:
                st.error("❌ You have reached the maximum number of attempts for this quiz.")
                return

            if None in st.session_state["user_answers"]:
                st.error("❌ Please answer all questions before submitting.")
                return

            score = sum(
                question["points"]
                for i, question in enumerate(questions)
                if st.session_state["user_answers"][i] == question["answer"]
            )

            st.session_state["attempts"] += 1
            
            # Display score with progress bar
            st.markdown("### Quiz Results")
            st.progress(score/100)
            st.success(f"📊 Your score: {score}/100")

            # Save grade to Google Sheets
            update_google_sheet(
                full_name="",
                email="",
                student_id=student_id,
                grade=score,
                current_assignment="quiz_2"
            )

if __name__ == "__main__":
    show()
