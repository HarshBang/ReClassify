import streamlit as st
import time
import bcrypt
# Predefined hashed passwords for authentication
hashed_passwords = {
    "pavani@nmims.in": "$2b$12$Ih6gyEcuygVFIJ4Jpbh9r.VLFYnJnAUelv52fUKkJqy8NjY2uU9MG",  # Hashed "1234"
    "chandrakant@nmims.in": "$2b$12$Ih6gyEcuygVFIJ4Jpbh9r.VLFYnJnAUelv52fUKkJqy8NjY2uU9MG",
    "vidyasagar@nmims.in": "$2b$12$Ih6gyEcuygVFIJ4Jpbh9r.VLFYnJnAUelv52fUKkJqy8NjY2uU9MG",
    "wasiha@nmims.in": "$2b$12$Ih6gyEcuygVFIJ4Jpbh9r.VLFYnJnAUelv52fUKkJqy8NjY2uU9MG",
    "vinayak@nmims.in": "$2b$12$Ih6gyEcuygVFIJ4Jpbh9r.VLFYnJnAUelv52fUKkJqy8NjY2uU9MG",
    "sanjay@nmims.in": "$2b$12$Ih6gyEcuygVFIJ4Jpbh9r.VLFYnJnAUelv52fUKkJqy8NjY2uU9MG"
}

# Role mapping for users
roles = {
    "pavani@nmims.in": "coordinator",
    "chandrakant@nmims.in": "schoolhead",
    "vidyasagar@nmims.in": "faculty",
    "wasiha@nmims.in": "faculty",
    "vinayak@nmims.in": "faculty",
    "sanjay@nmims.in" : "cr"
}

# Streamlit Page Configuration
st.set_page_config(page_title="ReClassify Login", page_icon="📅", layout="centered", initial_sidebar_state="collapsed")
st.set_page_config(page_title="ReClassify Login", page_icon="📅", layout="centered", initial_sidebar_state="collapsed")

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_email = ""

# Login Interface
if not st.session_state.authenticated:
    st.image("logo.png", width=300)
    st.title("ReClassify Login")

    email = st.text_input("Email ID", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login"):
        stored_hashed_password = hashed_passwords.get(email)
        if stored_hashed_password and bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
            st.session_state.authenticated = True
            st.session_state.user_email = email
        else:
            st.error("Invalid email or password. Please try again.")
else:
    # Display the main application content
    st.sidebar.success(f"Welcome, {st.session_state.user_email}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(authenticated=False, user_email=""))

    # Load the appropriate dashboard based on the user's role
    user_role = roles[st.session_state.user_email]
    if user_role == "coordinator":
        st.switch_page("pages/Coordinator_Dashboard.py")
    elif user_role == "schoolhead":
        st.switch_page("pages/Schoolhead_Dashboard.py")
    elif user_role == "faculty":
        st.switch_page("pages/Faculty_Dashboard.py")
    elif user_role == "cr":
        st.switch_page("pages/Cr_Dashboard.py")
