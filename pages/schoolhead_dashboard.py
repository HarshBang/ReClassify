import streamlit as st
import json
import pandas as pd

# Load JSON Data
def load_cancellation_data():
    with open("pages/cancellations.json", "r") as file:
        return json.load(file)

# Load faculty timetables
def load_faculty_timetable(filename):
    return pd.read_csv(filename, header=None)

# Load data
cancellation_data = load_cancellation_data()
timetable_rahul = load_faculty_timetable("rahul_timetable.csv")
timetable_vidyasagar = load_faculty_timetable("vidyasagar_timetable.csv")

# Convert JSON data into a structured DataFrame
cancellation_list = []

for faculty, schedule in cancellation_data.items():
    for day, times in schedule.items():
        for time_slot, details in times.items():
            cancellation_list.append({
                "Faculty": faculty,
                "Day": day,
                "Time Slot": time_slot,
                "Subject": details["subject"],
                "Leave Type": details["leave_type"]
            })

df_cancellation = pd.DataFrame(cancellation_list)

# Faculty List (Dropdown)
faculty_list = df_cancellation["Faculty"].unique().tolist()
selected_faculty = st.selectbox("Select a Faculty:", faculty_list)

# Display canceled classes and find available faculty
st.subheader(f"📌 Canceled Classes & Available Faculty for {selected_faculty}")

filtered_data = df_cancellation[df_cancellation["Faculty"] == selected_faculty]

if not filtered_data.empty:
    faculty_table = []

    # Days mapping to index positions
    days_mapping = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5
    }

    # Time Slot Mapping (Adjust based on CSV structure)
    time_slot_mapping = {
        "9:00 am to 10:00 am": 0,
        "10:00 am to 11:00 am": 1,
        "11:00 am to 12:00 pm": 2,
        "12:00 pm to 1:00 pm": 3,
        "1:00 pm to 2:00 pm": 4,
        "2:00 pm to 3:00 pm": 5
    }

    for _, row in filtered_data.iterrows():
        day_index = days_mapping.get(row["Day"], None)
        time_slot_index = time_slot_mapping.get(row["Time Slot"], None)

        if day_index is None or time_slot_index is None:
            continue  # Skip invalid entries

        # Check available faculty based on timetable
        available_faculty = []

        # Check if Rahul is free
        if timetable_rahul.iloc[day_index, time_slot_index] == "-":
            available_faculty.append("Dr. Rahul")

        # Check if Vidyasagar is free
        if timetable_vidyasagar.iloc[day_index, time_slot_index] == "-":
            available_faculty.append("Dr. Vidyasagar")

        faculty_table.append([
            row["Subject"],
            row["Day"],
            row["Time Slot"],
            ", ".join(available_faculty) if available_faculty else "None"
        ])

    faculty_df = pd.DataFrame(faculty_table, columns=["Subject", "Day", "Time Slot", "Available Faculty"])
    st.table(faculty_df)
else:
    st.warning("No cancellations found for this faculty.")