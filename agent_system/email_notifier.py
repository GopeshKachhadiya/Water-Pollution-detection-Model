import smtplib
import os
from email.message import EmailMessage

def send_email(report: str, image_path: str, authority_name: str):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("TEST_ALERT_EMAIL")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = f" Water Pollution Alert – {authority_name}"

    msg.set_content(f"""
Dear {authority_name},

A pollution event has been detected by the AI monitoring system.

Please find the incident report below:

{report}

Regards,
Water Pollution Detection AI
""")

    # Attach image if exists
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            img_data = f.read()

        msg.add_attachment(
            img_data,
            maintype="image",
            subtype="jpeg",
            filename=os.path.basename(image_path)
        )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        return {"status": "sent"}

    except Exception as e:
        return {"status": "failed", "error": str(e)}
