import streamlit as st
import pandas as pd
import smtplib
import os
from email.message import EmailMessage
from mail_template import User_data
from dotenv import load_dotenv, find_dotenv

if find_dotenv():
    load_dotenv()
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    APP_PASSWORD = os.getenv("APP_PASSWORD")
    APPLICATION_PASSWORD = os.getenv("APPLICATION_PASSWORD")
else:
    # Load password from Streamlit secrets
    APPLICATION_PASSWORD = st.secrets["authentication"]["APPLICATION_PASSWORD"]
    EMAIL_ADDRESS =st.secrets["authentication"]["EMAIL_ADDRESS"]
    APP_PASSWORD = st.secrets["authentication"]["APP_PASSWORD"]

# Check authentication status
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Authentication Page
if not st.session_state["authenticated"]:
    st.title("🔒 Login Required")
    password = st.text_input("Enter Password:", type="password")
    if st.button("Login"):
        #print(f"original - {password} and entered - {APPLICATION_PASSWORD}")
        if password == APPLICATION_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()  # Refresh the page after successful login
        else:
            st.error("❌ Incorrect Password. Try Again!")
    st.stop()  # Stop execution until login is successful


# Function to get recipients from Excel
def GetRecipients():
    EXCEL_PATH = "https://raw.githubusercontent.com/iamrishi-x/job_applicator_from_mailids/main/data/Mail_id.xlsx"
    df = pd.read_excel(EXCEL_PATH)
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
        st.write(f"###### Selected Cities: :blue[{', '.join(selected_cities)}]")
        st.write(f"###### Total Recipients: :red[{len(BCC_EMAILS)}]")

    return BCC_EMAILS

# Layout with Sidebar and Main Panel
st.set_page_config(page_title="Automated Email Sender", layout="wide")

# Sidebar - Sender Information and Resume Upload
st.sidebar.title("👤 Sender Information ")
sender_name = st.sidebar.text_input("Your Name:", value="Rushi Bagul")
sender_email = st.sidebar.text_input("Your Email Address:", value=EMAIL_ADDRESS)
app_password = st.sidebar.text_input("App Password:", value=APP_PASSWORD, type="password")
resume_file = st.sidebar.file_uploader("📄 Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# Main Panel - Email Subject and Body
st.title("📧 Automated Email Sender")

st.subheader("📌 Email Details")
subject, body = User_data(sender_name)
subject = st.text_input("Email Subject", value=subject)
body = st.text_area("Email Body", value=body, height=350)

st.markdown(
    """
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #0E1117; padding: 15px; text-align: center;">
        © <a href="https://github.com/iamrishi-x" target="_blank">Rishi Bagul</a> | Made with ❤️
    </div>
    """,
    unsafe_allow_html=True
)

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
            server.login(sender_email, app_password)
            server.send_message(msg)
            server.quit()
            st.success("✅ Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
