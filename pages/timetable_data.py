import json
import os

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


import json
import os

def load_csds_A1_2028():
    # Get the absolute path to the directory where this file resides
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to your JSON file
    file_path = os.path.join(base_dir, "csds_A1_2028.json")
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print("Error loading JSON:", e)
        return {}

