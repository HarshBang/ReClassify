import streamlit as st
import time

# Hide Streamlit sidebar using CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# User credentials
faculty_emails = {"vidyasagar@nmims.in", "wasiha@nmims.in", "vinayak@nmims.in"}
coordinator_email = "pavani@nmims.in"
schoolhead_email = "chandrakant@nmims.in"

# Streamlit Page Configuration
st.set_page_config(page_title="ReClassify Login", page_icon="📅", layout="centered")

# Centered Layout with Logo
st.image("logo.png", width=200)
st.title("ReClassify Login")

# Input Fields
email = st.text_input("Email ID", placeholder="Enter your email")
password = st.text_input("Password", type="password", placeholder="Enter your password")

# Login Button
if st.button("Login"):
    if email == coordinator_email and password == "1234":
        st.success("Logging in as Academic Coordinator...")
        time.sleep(1)
        st.switch_page("pages/academic_coordinator_app.py")
    elif email in faculty_emails and password == "1234":
        st.success(f"Logging in as Faculty ({email})...")
        time.sleep(1)
        st.switch_page("pages/faculty_dashboard.py")
    elif email == schoolhead_email and password == "1234":
        st.success("Logging in as School Head...")
        time.sleep(1)
        st.switch_page("pages/schoolhead_dashboard.py")
    else:
        st.error("Invalid email or password. Please try again.")
