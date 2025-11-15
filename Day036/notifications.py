"""Notification module supporting SMS (Twilio) and Email.

Sends alerts about stock price changes and news.
"""
from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Optional


def env_bool(key: str, default: bool = False) -> bool:
    """Parse environment variable as boolean."""
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


def send_sms(message: str) -> bool:
    """Send SMS via Twilio.
    
    Requires: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_FROM, TWILIO_PHONE_TO
    Returns True on success, False on failure.
    """
    try:
        from twilio.rest import Client
    except ImportError:
        print("[ERROR] Twilio library not installed. Run: pip install twilio")
        return False
    
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_FROM")
    to_phone = os.getenv("TWILIO_PHONE_TO")
    
    if not all([account_sid, auth_token, from_phone, to_phone]):
        print("[ERROR] Missing Twilio credentials in environment")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        print(f"[SMS SENT] SID: {msg.sid}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send SMS: {e}")
        return False


def send_email(subject: str, body: str) -> bool:
    """Send email notification.
    
    Requires: EMAIL_USER, EMAIL_PASS, TO_EMAIL (optional), SMTP_SERVER, SMTP_PORT
    Returns True on success, False on failure.
    """
    server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    use_tls = env_bool("USE_TLS", True)
    user = os.getenv("EMAIL_USER")
    pwd = os.getenv("EMAIL_PASS")
    to_addr = os.getenv("TO_EMAIL") or user
    from_name = os.getenv("FROM_NAME", "Stock Monitor")
    
    if not user or not pwd:
        print("[ERROR] EMAIL_USER and EMAIL_PASS must be set")
        return False
    
    try:
        msg = EmailMessage()
        msg["From"] = f"{from_name} <{user}>"
        msg["To"] = to_addr
        msg["Subject"] = subject
        msg.set_content(body)
        
        with smtplib.SMTP(server, port, timeout=30) as smtp:
            smtp.ehlo()
            if use_tls:
                smtp.starttls()
                smtp.ehlo()
            smtp.login(user, pwd)
            smtp.send_message(msg)
        
        print(f"[EMAIL SENT] to {to_addr}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False


def send_notification(subject: str, message: str, use_sms: bool = False) -> bool:
    """Send notification via SMS or Email based on preference.
    
    Args:
        subject: Email subject (ignored for SMS)
        message: Message body
        use_sms: If True, send SMS; otherwise send email
    
    Returns True if sent successfully.
    """
    if use_sms:
        return send_sms(message)
    else:
        return send_email(subject, message)


if __name__ == "__main__":
    # Test
    test_subject = "Test Stock Alert"
    test_message = "TSLA: 🔺 5.2%\n\nThis is a test notification from the stock monitor."
    
    use_sms = env_bool("USE_SMS", False)
    
    print(f"Sending test notification via {'SMS' if use_sms else 'Email'}...")
    success = send_notification(test_subject, test_message, use_sms)
    
    if success:
        print("✅ Test notification sent!")
    else:
        print("❌ Test notification failed")
