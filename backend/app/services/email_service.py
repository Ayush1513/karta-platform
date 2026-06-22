import os
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_otp_email(
    receiver_email: str,
    otp: str
):

    try:

        subject = "Karta Password Reset OTP"

        body = f"""
Hello,

Your OTP is: {otp}

This OTP is valid for password reset.

Karta Platform
"""

        message = MIMEMultipart()

        message["From"] = EMAIL_ADDRESS
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(
            MIMEText(body, "plain")
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            receiver_email,
            message.as_string()
        )

        server.quit()

        return True

    except Exception as e:

        print("Email Error:", e)

        return False