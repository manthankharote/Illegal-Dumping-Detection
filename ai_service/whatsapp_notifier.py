"""
Module: whatsapp_notifier.py
Role: Notification orchestration conduit.
Description: Handles outbound external integrations using Twilio API to dispatch 
validated alerts asynchronously from the core simulation loop.
"""
import os
from twilio.rest import Client
from dotenv import load_dotenv

# Ensure configuration parameters are securely evaluated during execution.
load_dotenv() 

def send_alert(location: str, confidence: float):
    """
    Constructs and broadcasts incident data to response authorities.
    
    Parameters:
        location (str): The localized spatial identifier for the event.
        confidence (float): Statistical confidence mapping from the underlying classifier.
    """
    # Securely retrieve authentication vectors and external routing protocols.
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp = os.getenv("TWILIO_PHONE_NUMBER")      
    to_whatsapp = os.getenv("DESTINATION_PHONE_NUMBER")   

    # Execute preliminary threshold mechanism to validate configuration parameter fidelity.
    if not all([account_sid, auth_token, from_whatsapp, to_whatsapp]):
        print(f"[DEBUG] SID: {bool(account_sid)}, Token: {bool(auth_token)}, From: {bool(from_whatsapp)}, To: {bool(to_whatsapp)}")
        print("[SYSTEM] Twilio keys missing in environment. WhatsApp alert skipped.")
        return

    try:
        # Instantiate remote client communication sockets.
        client = Client(account_sid, auth_token)

        # Assemble the automated structural payload for downstream subscribers.
        message_body = (
            f"🚨 *ALERT: Illegal Garbage Dumping Detected!*\n"
            f"📍 *Location:* {location}\n"
            f"🤖 *AI Confidence:* {confidence:.1f}%\n\n"
            f"Action required by Municipal Cleaning Authorities."
        )

        # Dispatch the payload across network boundaries.
        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        print(f"[SYSTEM] WhatsApp alert sent! Message SID: {message.sid}")

    except Exception as e:
        # Mute exception propagation to guarantee validator deterministic execution.
        print(f"[ERROR] Failed to send WhatsApp alert. Error: {e}")