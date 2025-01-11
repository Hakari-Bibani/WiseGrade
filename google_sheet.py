import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and connect to Google Sheets API
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_credentials"], scope)
    client = gspread.authorize(creds)
    return client

# Save data for the first assignment
def save_first_assignment(data):
    client = authenticate_google_sheets()
    sheet = client.open("WG").sheet1  # Replace with your sheet name
    sheet.append_row([
        data["full_name"],
        data["email"],
        data["student_ID"],
        data["assignment_1"],  # Grade for Assignment 1
        "",  # Placeholder for Assignment 2
        "",  # Placeholder for Assignment 3
        "",  # Placeholder for Assignment 4
        "",  # Placeholder for Quiz 1
        "",  # Placeholder for Quiz 2
        "",  # Placeholder for Quiz 3
        "",  # Placeholder for Quiz 4
        data["assignment_1"]  # Total (initially just Assignment 1 grade)
    ])

# Update data for subsequent assignments or quizzes
def update_record(student_id, assignment_name, grade):
    client = authenticate_google_sheets()
    sheet = client.open("WG").sheet1  # Replace with your sheet name
    records = sheet.get_all_records()

    # Find the row corresponding to the student_id
    for i, record in enumerate(records):
        if record["student_ID"] == student_id:
            row_index = i + 2  # Rows are 1-indexed, and header is row 1
            # Update the specific assignment or quiz column
            if assignment_name.startswith("assignment"):
                col_index = sheet.find(assignment_name).col
            elif assignment_name.startswith("quiz"):
                col_index = sheet.find(assignment_name).col
            else:
                raise ValueError("Invalid assignment or quiz name")

            # Update the grade
            sheet.update_cell(row_index, col_index, grade)

            # Update the total grade
            total = sum(float(record.get(col, 0)) for col in [
                "assignment_1", "assignment_2", "assignment_3", "assignment_4",
                "quiz_1", "quiz_2", "quiz_3", "quiz_4"
            ])
            sheet.update_cell(row_index, sheet.find("total").col, total)
            break
    else:
        raise ValueError("Student ID not found in records")
