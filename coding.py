import streamlit as st
import pandas as pd
import smtplib
import os
from email.message import EmailMessage
from mail_template import User_data
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

# Function to get recipients from Excel
def GetRecipients():
    EXCEL_PATH = r"data\Mail_id.xlsx"
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    st.subheader("Select Cities for Recipients")
    city_list = list(df.columns)
    selected_cities = st.multiselect("Choose Cities:", city_list)

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

st.title("Automated Email Sender")

# Input fields for email sender details
sender_email = st.text_input("Your Email Address:")
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
subject = st.text_input("Email Subject", value=User_data.subject)
body = st.text_area("Email Body", value=User_data.body)

# Get recipients
BCC_EMAILS = GetRecipients()

# Send email button
if st.button("Send Emails"):
    if not sender_email or not resume_file or not BCC_EMAILS:
        st.error("Please provide all required inputs.")
    else:
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = sender_email
        msg["Bcc"] = ", ".join(BCC_EMAILS)
        msg["Subject"] = subject
        msg.set_content(body)

        msg.add_attachment(resume_file.read(), maintype="application", subtype="pdf", filename=resume_file.name)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, APP_PASSWORD)
            server.send_message(msg)
            server.quit()
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")
