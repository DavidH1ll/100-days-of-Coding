import os

try:
    from twilio.rest import Client
except Exception:
    Client = None

TWILIO_SID = os.getenv("TWILIO_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN", "")
TWILIO_FROM = os.getenv("TWILIO_FROM", "")
TWILIO_TO = os.getenv("ALERT_TO", "")

class NotificationManager:
    def __init__(self):
        self.enabled = all([Client, TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, TWILIO_TO])
        self.client = Client(TWILIO_SID, TWILIO_TOKEN) if self.enabled else None

    def send(self, message: str):
        if not self.enabled:
            print(f"[SMS disabled] {message}")
            return
        self.client.messages.create(body=message, from_=TWILIO_FROM, to=TWILIO_TO)