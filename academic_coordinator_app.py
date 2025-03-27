import streamlit as st
import pandas as pd
import timetable_data  # Import the storage script

# Batch & Faculty Data
batch_list = [
    "Batch 2028: CDDS A1", "Batch 2028: CDDS A2", "Batch 2028: CDDS B1", "Batch 2028: CDDS B2",
    "Batch 2028: CE C1", "Batch 2028: CE C2", "Batch 2027: CDDS", "Batch 2027: CE", "Batch 2026: CDDS"
]
faculty_list = ["Dr. V Vidyasagar", "Dr. Rahul Koshti", "Wasiha Tasneem"]

# Column & Row Headers
column_headers = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
row_headers = [
    "9:00 am to 10:00 am", "10:00 am to 11:00 am", "11:00 am to 12:00 pm", "12:00 pm to 1:00 pm",
    "2:00 pm to 3:00 pm", "3:00 pm to 4:00 pm", "4:00 pm to 5:00 pm", "5:00 pm to 6:00 pm"
]

# 🔄 Load Stored Timetables
timetable = timetable_data.load_timetable()
faculty_timetable = timetable_data.load_faculty_timetable()

st.title("Academic Coordinator Dashboard")
st.sidebar.image("logo.png", use_container_width=True)  # Display Logo

# ---- Radio Button for Selection ----
selection = st.radio("Choose Upload Type", ["Upload Student Timetable", "Upload Faculty Timetable"])

# ---- Student Timetable Section ----
if selection == "Upload Student Timetable":
    st.subheader("📤 Upload Timetable for Batch & Section")
    batch_section = st.selectbox("Select Batch & Section", batch_list)
    uploaded_file = st.file_uploader("Upload Batch Timetable (CSV)", type=["csv"], key="batch_csv")

    if st.button("Upload Timetable"):
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, header=None)
            df.columns = column_headers  # Assign days as column headers
            df.insert(0, "Timings", row_headers)  # Insert row headers (Timings)
            timetable[batch_section] = df.values.tolist()  # Convert dataframe to list and store
            timetable_data.save_timetable(timetable)  # Save to storage
            st.success(f"✅ Timetable uploaded for {batch_section}!")

    # Display Batch Timetable
    st.subheader(f"📌 Current Timetable for {batch_section}")
    if batch_section in timetable:
        df_display = pd.DataFrame(timetable[batch_section], columns=["Timings"] + column_headers)
        st.table(df_display)
    else:
        st.warning(f"No timetable uploaded for {batch_section}")

# ---- Faculty Timetable Section ----
elif selection == "Upload Faculty Timetable":
    st.subheader("📤 Upload Faculty Timetable")
    faculty_name = st.selectbox("Select Faculty", faculty_list)
    uploaded_faculty_file = st.file_uploader("Upload Faculty Timetable (CSV)", type=["csv"], key="faculty_csv")

    if st.button("Upload Faculty Timetable"):
        if uploaded_faculty_file is not None:
            df_faculty = pd.read_csv(uploaded_faculty_file, header=None)
            df_faculty.columns = column_headers
            df_faculty.insert(0, "Timings", row_headers)
            faculty_timetable[faculty_name] = df_faculty.values.tolist()
            timetable_data.save_faculty_timetable(faculty_timetable)
            st.success(f"✅ Timetable uploaded for {faculty_name}!")

    # Display Faculty Timetable
    st.subheader(f"📌 Current Timetable for {faculty_name}")
    if faculty_name in faculty_timetable:
        df_faculty_display = pd.DataFrame(faculty_timetable[faculty_name], columns=["Timings"] + column_headers)
        st.table(df_faculty_display)
    else:
        st.warning(f"No timetable uploaded for {faculty_name}")
