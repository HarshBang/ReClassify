import pandas as pd
import streamlit as st
import json
st.set_page_config(initial_sidebar_state="collapsed")
st.sidebar.image("logo.png")  # Display Logo
st.image("logo.png", width = 300)

FACULTY_TIMETABLE_FILE = "pages/faculty_timetable.json"
CANCELLATION_FILE = "pages/cancellations.json"

faculty_emails = {
    "vidyasagar@nmims.edu": "Dr. V Vidyasagar",
    "wasiha@nmims.edu": "Wasiha Tasneem",
    "vinayak@nmims.edu": "Vinayak Mukkawar"
}

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
slots = [
    "9:00 am to 10:00 am", "10:00 am to 11:00 am", "11:00 am to 12:00 pm", "12:00 pm to 1:00 pm",
    "2:00 pm to 3:00 pm", "3:00 pm to 4:00 pm", "4:00 pm to 5:00 pm", "5:00 pm to 6:00 pm"
]

leave_types = [
    "Personal Leave", 
    "Official Leave In-campus", 
    "Official Leave Out-campus"
]

def load_faculty_timetable():
    try:
        with open(FACULTY_TIMETABLE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_cancellations():
    try:
        with open(CANCELLATION_FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_cancellations(cancellations):
    with open(CANCELLATION_FILE, "w") as file:
        json.dump(cancellations, file, indent=4)

def get_available_faculty(cancel_day, cancel_slot, faculty_name):
    """
    Find available faculty who have "-" in their timetable for the given day and slot.
    """
    faculty_timetable = load_faculty_timetable()
    available_faculty = []

    for other_faculty, timetable in faculty_timetable.items():
        if other_faculty != faculty_name:  # Exclude current faculty
            df_other = pd.DataFrame([row[1:] for row in timetable], index=slots, columns=days)
            if df_other.at[cancel_slot, cancel_day] == "-":
                available_faculty.append(other_faculty)

    return available_faculty

def faculty_dashboard(email):
    st.title("📚 Faculty Dashboard")

    faculty_name = faculty_emails.get(email, "Unknown Faculty")
    if faculty_name == "Unknown Faculty":
        st.error("⚠ Faculty not recognized!")
        return

    st.subheader(f"Welcome, {faculty_name}")

    faculty_timetable = load_faculty_timetable()
    cancellations = load_cancellations()

    if faculty_name in faculty_timetable:
        st.subheader("📅 Regular Timetable (Unchanged)")
        timetable_data = faculty_timetable[faculty_name]
        df_timetable = pd.DataFrame([row[1:] for row in timetable_data], index=slots, columns=days)
        
        faculty_cancellations = cancellations.get(faculty_name, {})
        df_updated_timetable = df_timetable.copy()

        for day, canceled_slots in faculty_cancellations.items():
            for slot, info in canceled_slots.items():
                df_updated_timetable.at[slot, day] = "❌"

        st.table(df_timetable)  
        st.subheader("📅 Updated Timetable (After Cancellations)")
        st.table(df_updated_timetable)  

        st.subheader("🛑 Cancel a Class")
        cancel_day = st.selectbox("Select Day to Cancel", days)
        available_slots = [slot for slot in slots if df_timetable.at[slot, cancel_day] not in ["-", "❌"]]

        if available_slots:
            cancel_type = st.radio("Cancel:", ["Single Slot", "Whole Day"])
            if cancel_type == "Single Slot":
                cancel_slot = st.selectbox("Select Time Slot", available_slots)
                cancel_reason = st.selectbox("Reason for Cancellation", leave_types)

                if st.button("Cancel Class"):
                    subject = df_timetable.at[cancel_slot, cancel_day]
                    if faculty_name not in cancellations:
                        cancellations[faculty_name] = {}
                    if cancel_day not in cancellations[faculty_name]:
                        cancellations[faculty_name][cancel_day] = {}

                    if cancel_slot in cancellations[faculty_name][cancel_day]:
                        st.warning(f"⚠ {cancel_slot} on {cancel_day} is already canceled!")
                    else:
                        cancellations[faculty_name][cancel_day][cancel_slot] = {
                            "subject": subject,
                            "leave_type": cancel_reason  
                        }
                        save_cancellations(cancellations)
                        st.success(f"✅ {cancel_slot} on {cancel_day} canceled successfully!")
                        st.rerun()

            elif cancel_type == "Whole Day":
                cancel_reason = st.selectbox("Reason for Cancellation", leave_types)
                if st.button("Cancel All Classes for the Day"):
                    if faculty_name not in cancellations:
                        cancellations[faculty_name] = {}
                    if cancel_day not in cancellations[faculty_name]:
                        cancellations[faculty_name][cancel_day] = {}

                    for slot in available_slots:
                        subject = df_timetable.at[slot, cancel_day]
                        if slot not in cancellations[faculty_name][cancel_day]:
                            cancellations[faculty_name][cancel_day][slot] = {
                                "subject": subject,
                                "leave_type": cancel_reason  
                            }

                    save_cancellations(cancellations)
                    st.success(f"✅ All classes on {cancel_day} canceled successfully!")
                    st.rerun()

        else:
            st.warning("No classes available to cancel for the selected day.")

        ## ------------------------------ REQUEST FACULTY TO TAKE CLASS ------------------------------ ##
        st.subheader("🔄 Request Faculty to Take Class")
        
        # Get list of already canceled classes
        canceled_classes = []
        for day, slots_data in faculty_cancellations.items():
            for slot, info in slots_data.items():
                canceled_classes.append(f"{day} - {slot} ({info['subject']})")

        if canceled_classes:
            selected_cancel_class = st.selectbox("Select a canceled class", canceled_classes)
            cancel_day, cancel_slot_info = selected_cancel_class.split(" - ")
            cancel_slot = cancel_slot_info.split(" (")[0]  # Extract slot time

            available_faculty = get_available_faculty(cancel_day, cancel_slot, faculty_name)

            if available_faculty:
                selected_faculty = st.selectbox("Select Faculty to Request", available_faculty)
                if st.button("Send Request"):
                    st.success(f"✅ Request sent to {selected_faculty} for {cancel_slot} on {cancel_day}")
            else:
                st.warning("⚠ No available faculty for this slot.")

    else:
        st.warning("No timetable found for you!")

faculty_dashboard(email="wasiha@nmims.edu")


# -- logout button --
if st.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.user_email = ""
    st.switch_page("app.py")