import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from pages.timetable_data import load_csds_A1_2028

st.set_page_config(page_title="CR Dashboard", layout="wide", initial_sidebar_state="collapsed")
st.title("📌 Class Representative Dashboard")
st.sidebar.image("logo.png") 
st.sidebar.title("CR Dashboard")

st.image("logo.png", width = 300)

batch_section = st.selectbox("Select Class", ["CSDS A1 | Year: 2028"])

# Load Stored Timetable Data
timetable = load_csds_A1_2028()

# Extract class and year from selectbox string and form the key
class_part, year_part = batch_section.split("|")
class_part = class_part.strip()        # "CSDS A1"
year_part = year_part.split(":")[1].strip()  # "2028"
batch_section_key = f"Batch {year_part}: {class_part}"

# 📅 Timetable Section

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


if batch_section_key in timetable and "timetable" in timetable[batch_section_key]:
    df_timetable = pd.DataFrame(timetable[batch_section_key]["timetable"])

    # Display timetable with days as headings
    st.write("### 📅 Your Weekly Timetable")
    cols = st.columns(6)

    # Create the header row (days of the week)
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"### {day}")

# Display timetable with faculty details
    for index, row in df_timetable.iterrows():
        timing = row['Timings']

        # Check if this row represents Lunch Break
        if all(row[day].get("subject", "") == "Lunch Break" for day in days):
            st.markdown(
                f"""<div style=" text-align: center; padding: 8px; border-radius: 8px;">
                <b> ⏰ {timing} - 🍽️ Lunch Break </b>
                </div>""",
                unsafe_allow_html=True
            )
        else:
            # Normal row with 6 columns
            st.write(f"⏰ {timing}")
            cols = st.columns(6)

            for i, day in enumerate(days):
                details = row.get(day, {})
                subject = details.get("subject", "-")
                faculty = details.get("faculty", "Unknown")
                location = details.get("location", "Unknown")

                with cols[i]:
                    if subject and subject != "Lunch Break":
                        with st.expander(f"📖 {subject}"): 
                             st.markdown(f"**👨‍🏫 Faculty:** {faculty}  \n**📍 Location:** {location}")
                    else:
                        st.write(subject)


    # Create a simplified DataFrame with only Timings and Subjects
    simplified_timetable = df_timetable[['Timings'] + days].copy()

    for day in days:
        simplified_timetable[day] = simplified_timetable[day].apply(lambda x: x.get('subject', '-') if isinstance(x, dict) else '-')


    # Function to convert DataFrame to CSV
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    # Convert the simplified timetable to CSV
    csv_data = convert_df_to_csv(simplified_timetable)

    # Download button
    st.download_button(
        label="Download Timetable as CSV",
        data=csv_data,
        file_name=f"{class_part}_{year_part}_Timetable.csv",
        mime='text/csv',
    )

else:
    st.warning(f"No timetable uploaded for {batch_section_key}")



# -- Notification System with Email --
st.subheader("📢 Notifications")

# Initialize notifications in session state if not exists
if "notifications" not in st.session_state:
    st.session_state.notifications = []

# Function to send an email notification
def send_email_notification(subject, message):
    sender_email = "reclassify27@gmail.com"  # Your email
    sender_password = "kbgh uzeh auya wwar"  
    recipient_email = "ashisharma0507@gmail.com"  # Academic Coordinator's email

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Input for new notification
show_options = st.expander("Write a message to the Academic Coordinator: ")

with show_options:
    new_notification = st.text_area("Address your requests here!! ")

    if st.button("Send Message"):
        if new_notification.strip():
            st.session_state.notifications.append(new_notification)
            
            # Send email
            subject = "New Notification from CR"
            message = f"Dear Academic Coordinator,\n\nYou have a new message from the Class Representative:\n\n{new_notification}\n\nBest regards,\nCSDS A1, \n1st Year, \nCR Dashboard"
            
            if send_email_notification(subject, message):
                st.success("Message sent successfully!")
            else:
                st.error("Failed to send the message via email.")
        else:
            st.warning("Messages cannot be empty!")

    # Display existing notifications
    if st.session_state.notifications:
        for notification in reversed(st.session_state.notifications):
            st.info(notification)
    else:
        st.write("No notifications yet.")


# -- Logout button --
if st.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.user_email = ""
    st.switch_page("app.py")