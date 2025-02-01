import streamlit as st
import pandas as pd
import smtplib
import os
from email.message import EmailMessage
from mail_template import User_data
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve email and password from environment variables
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

# Function to get recipients from Excel
def GetRecipients():
    #EXCEL_PATH = r"data\Mail_id.xlsx"
    #file = st.sidebar.file_uploader("Upload Excel or CSV File with Emails", type=["xlsx", "csv"])
    EXCEL_PATH = r"data\Mail_id.xlsx"
    # Read the Excel file and clean column names
    df = pd.read_excel(EXCEL_PATH)
    # df = pd.DataFrame()
    # if file:
    #     if file.name.endswith(".xlsx"):
    #         df = pd.read_excel(file)
    #     elif file.name.endswith(".csv"):
    #         df = pd.read_csv(file)
    df.columns = df.columns.astype(str).str.strip()

    st.sidebar.subheader("Select Cities for Recipients")
    city_list = list(df.columns)
    selected_cities = st.sidebar.multiselect("Choose Cities:", city_list)

    BCC_EMAILS = []
    for city in selected_cities:
        if city in df.columns:
            BCC_EMAILS.extend(df[city].dropna().tolist())
    
    BCC_EMAILS = list(set(BCC_EMAILS))

    if BCC_EMAILS:
        st.write(f"### Selected Cities: {', '.join(selected_cities)}")
        st.write(f"### Total Recipients: {len(BCC_EMAILS)}")
        st.dataframe(pd.DataFrame({"Recipients": BCC_EMAILS}))

    return BCC_EMAILS

# Layout with Sidebar and Main Panel
st.set_page_config(page_title="Automated Email Sender", layout="wide")

# Sidebar - Sender Information and Resume Upload
st.sidebar.title("Navigation")
st.sidebar.subheader("Sender Information")
sender_name = st.sidebar.text_input("Your Name:")
sender_email = st.sidebar.text_input("Your Email Address:", value=EMAIL_ADDRESS)
app_password = st.sidebar.text_input("App Password:", value=APP_PASSWORD, type="password")
resume_file = st.sidebar.file_uploader("📄 Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# Main Panel - Email Subject and Body
st.title("📧 Automated Email Sender")

st.subheader("📌 Email Details")
subject,body = User_data(sender_name)
subject = st.text_input("Email Subject", value=subject)
body = st.text_area("Email Body", value=body, height=350)

# Get recipients
BCC_EMAILS = GetRecipients()

# Send email button
if st.button("🚀 Send Emails"):
    if not sender_email or not app_password or not resume_file or not BCC_EMAILS:
        st.error("⚠️ Please provide all required inputs.")
    else:
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = sender_email
        msg["Bcc"] = ", ".join(BCC_EMAILS)
        msg["Subject"] = subject
        msg.set_content(body)

        # Attach resume file
        file_data = resume_file.read()
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=resume_file.name)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)  # Use sender's email and app password for login
            server.send_message(msg)
            server.quit()
            st.success("✅ Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
