import smtplib
import os
from email.message import EmailMessage
from mail_template import User_data
from dotenv import load_dotenv
from FromHRExcelList import GetRecipients
load_dotenv()  # Take environment variables from .env.
# Your email credentials

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

# Email details
BCC_EMAILS = GetRecipients()

SUBJECT = User_data.subject 
BODY = User_data.body

# Create email message
msg = EmailMessage()
msg["From"] = EMAIL_ADDRESS
msg["To"] = EMAIL_ADDRESS
msg["Bcc"] = ", ".join(BCC_EMAILS)  # Add recipients in BCC (hidden)
msg["Subject"] = SUBJECT
msg.set_content(BODY)

# Attach resume (ensure the file path is correct)
RESUME_PATH = r"dataRushi-Bagul-Genai.pdf"  # Change this to your resume path
if os.path.exists(RESUME_PATH):
    with open(RESUME_PATH, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="Rushi-Bagul-Genai.pdf")
else:
    print("Resume file not found!")

input(f"Do you want to send mail to all {len(BCC_EMAILS)} recipients? (Press Enter to continue) ... ")

print(f"""Sending mail to {len(BCC_EMAILS)} recipients...""")
# Send email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, APP_PASSWORD)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")