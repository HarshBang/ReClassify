import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
st.set_page_config(initial_sidebar_state="collapsed")
st.sidebar.image("logo.png") 
st.image("logo.png", width = 300)
# Load JSON Data
def load_json(filename):
    with open(filename, "r") as file:
def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)

# Load data
cancellation_data = load_json("pages/cancellations.json")
faculty_timetable = load_json("pages/faculty_timetable.json")
cancellation_data = load_json("pages/cancellations.json")
faculty_timetable = load_json("pages/faculty_timetable.json")

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
    days_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5}
    days_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5}

    for _, row in filtered_data.iterrows():
        day_index = days_mapping.get(row["Day"], None)
        time_slot = row["Time Slot"]
        
        if day_index is None:
        time_slot = row["Time Slot"]
        
        if day_index is None:
            continue  # Skip invalid entries

        available_faculty = []
        
        # Check each faculty's timetable
        for faculty, schedule in faculty_timetable.items():
            if time_slot in [slot[0] for slot in schedule]:  # Ensure time slot exists
                time_slot_index = [slot[0] for slot in schedule].index(time_slot)
                
                if schedule[time_slot_index][day_index + 1] == "-":  # Check if slot is free
                    available_faculty.append(faculty)
        
        
        # Check each faculty's timetable
        for faculty, schedule in faculty_timetable.items():
            if time_slot in [slot[0] for slot in schedule]:  # Ensure time slot exists
                time_slot_index = [slot[0] for slot in schedule].index(time_slot)
                
                if schedule[time_slot_index][day_index + 1] == "-":  # Check if slot is free
                    available_faculty.append(faculty)
        
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

# ---- 📊 ADDING VISUALIZATION ----
st.subheader("📊 Cancellations by Day & Type")

# Process data for visualization
cancellations_by_day = defaultdict(lambda: {"Official Leave": 0, "Personal Leave": 0})

for person, schedule in cancellation_data.items():
    for day, sessions in schedule.items():
        for time, details in sessions.items():
            leave_type = details["leave_type"]
            category = "Official Leave" if "Official" in leave_type else "Personal Leave"
            cancellations_by_day[day][category] += 1

# Prepare data for plotting
days = list(cancellations_by_day.keys())
official_leaves = [cancellations_by_day[day]["Official Leave"] for day in days]
personal_leaves = [cancellations_by_day[day]["Personal Leave"] for day in days]

# Display in Streamlit
# 1️⃣ Cancellations by Day and Type
cancellations_by_day = defaultdict(lambda: {"Official Leave": 0, "Personal Leave": 0})
for _, row in df_cancellation.iterrows():
    category = "Official Leave" if "Official" in row["Leave Type"] else "Personal Leave"
    cancellations_by_day[row["Day"]][category] += 1

days = list(cancellations_by_day.keys())
official_leaves = [cancellations_by_day[day]["Official Leave"] for day in days]
personal_leaves = [cancellations_by_day[day]["Personal Leave"] for day in days]

fig, ax = plt.subplots(figsize=(8, 4))  # Smaller Size
ax.bar(days, official_leaves, label="Official Leave", color="blue")
ax.bar(days, personal_leaves, bottom=official_leaves, label="Personal Leave", color="red")

ax.set_ylabel("Number of Cancellations")
ax.set_title("Cancellations by Day and Type")
ax.legend()
plt.xticks(rotation=0)  # Labels Horizontal
st.pyplot(fig)


# JSON data
data = {
    "Wasiha Tasneem": {
        "Monday": {
            "10:00 am to 11:00 am": {
                "subject": "ADSA",
                "leave_type": "Official Leave In-campus"
            }
        },
        "Thursday": {
            "10:00 am to 11:00 am": {
                "subject": "PDA LAB B2",
                "leave_type": "Personal Leave"
            },
            "11:00 am to 12:00 pm": {
                "subject": "PDA LAB B2",
                "leave_type": "Personal Leave"
            },
            "12:00 pm to 1:00 pm": {
                "subject": "DBMS",
                "leave_type": "Personal Leave"
            },
            "2:00 pm to 3:00 pm": {
                "subject": "DAA",
                "leave_type": "Personal Leave"
            }
        }
    }
}

# Extracting subject-wise pending class count
subject_counts = {}

for faculty, schedule in data.items():
    for day, slots in schedule.items():
        for time_slot, details in slots.items():
            subject = details["subject"]
            subject_counts[subject] = subject_counts.get(subject, 0) + 1

# Pie Chart - Pending Classes Count per Subject
plt.figure(figsize=(6, 6))
plt.pie(subject_counts.values(), labels=[f"{sub} ({cnt})" for sub, cnt in subject_counts.items()], 
        colors=['lightblue', 'orange', 'lightgreen', 'red'], autopct="%1.1f%%", startangle=140)
plt.title("Pending Classes Count per Subject")
st.pyplot(plt)



# 4️⃣ Cancellations per Subject
fig, ax = plt.subplots(figsize=(8, 4))  # Smaller Size
subject_counts = df_cancellation["Subject"].value_counts()
sns.barplot(x=subject_counts.index, y=subject_counts.values, ax=ax, palette="viridis")

ax.set_ylabel("Cancellations")
ax.set_xlabel("Subject")
ax.set_title("Cancellations per Subject")
plt.xticks(rotation=0)  # Labels Horizontal
st.pyplot(fig)

# -- logout button --
if st.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.user_email = ""
    st.switch_page("app.py")