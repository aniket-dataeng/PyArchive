import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        self.recipient_email = os.getenv("EMAIL_RECIPIENT")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.logger = logging.getLogger("logger")

    def send_email(self, subject, body, attachment_path=None):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        self.logger.info(msg["From"])
        if attachment_path:
            if os.path.exists(attachment_path):  # Ensure file exists
                try:
                    with open(attachment_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
                        msg.attach(part)
                    self.logger.info(f"Attached file: {attachment_path}")
                except Exception as e:
                    self.logger.error(f"Failed to attach file: {e}")
            else:
                self.logger.warning(f"File not found: {attachment_path}")

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            self.logger.info("Email sent successfully!")
        except Exception as e:
            self.logger.info(f"Failed to send email: {str(e)}") 
