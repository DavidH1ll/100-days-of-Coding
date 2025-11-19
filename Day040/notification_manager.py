import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from twilio.rest import Client
except Exception:
    Client = None

# Twilio config
TWILIO_SID = os.getenv("TWILIO_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN", "")
TWILIO_FROM = os.getenv("TWILIO_FROM", "")
TWILIO_TO = os.getenv("ALERT_TO", "")

# Email config
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USER)


class NotificationManager:
    def __init__(self):
        self.twilio_enabled = all([Client, TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, TWILIO_TO])
        self.email_enabled = all([EMAIL_USER, EMAIL_PASSWORD])
        
        if self.twilio_enabled:
            self.twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)
    
    def send_sms(self, message: str):
        """Send SMS via Twilio (original Day 39 functionality)."""
        if not self.twilio_enabled:
            print(f"[SMS disabled] {message}")
            return
        
        self.twilio_client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
    
    def send_email(self, to_email: str, subject: str, body: str):
        """Send email via SMTP."""
        if not self.email_enabled:
            print(f"[Email disabled] Would send to {to_email}: {subject}")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_FROM
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
        
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")