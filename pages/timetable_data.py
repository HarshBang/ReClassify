import json

# Storage files
STUDENT_TIMETABLE_FILE = "student_timetable.json"
FACULTY_TIMETABLE_FILE = "faculty_timetable.json"

# ---- Load Student Timetable ----
def load_timetable():
    try:
        with open(STUDENT_TIMETABLE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return an empty dictionary if no data

# ---- Save Student Timetable ----
def save_timetable(timetable):
    with open(STUDENT_TIMETABLE_FILE, "w") as file:
        json.dump(timetable, file, indent=4)

# ---- Load Faculty Timetable ----
def load_faculty_timetable():
    try:
        with open(FACULTY_TIMETABLE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# ---- Save Faculty Timetable ----
def save_faculty_timetable(faculty_timetable):
    with open(FACULTY_TIMETABLE_FILE, "w") as file:
        json.dump(faculty_timetable, file, indent=4)
