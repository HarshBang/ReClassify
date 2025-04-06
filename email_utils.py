import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

# Load email config
def load_config():
    try:
        with open("config.json", "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"⚠️ Failed to load email config: {e}")
        return None

# Send Email Function (with debugging)
def send_email(subject, html_content):
    """Send email and print debug info."""
    config = load_config()
    if not config:
        st.error("⚠️ Email configuration missing!")
        return False

    try:
        print("📧 Connecting to SMTP Server...")
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        print("✅ Connection successful!")

        print(f"📧 Logging in as: {config['sender_email']}")
        server.login(config['sender_email'], config['sender_password'])

        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['To'] = config['faculty_email']
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        print(f"📤 Sending email to: {config['faculty_email']}")
        server.sendmail(config['sender_email'], config['faculty_email'], msg.as_string())
        server.quit()
        
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        st.error(f"❌ Email failed to send: {e}")
        return False
