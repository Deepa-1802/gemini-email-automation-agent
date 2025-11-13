from clients.gemini_client import client
from google.genai import types
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

def generate_reply(email, category):
    prompt = f"""
Draft a polite and concise reply to the following email.
Category: {category}
Subject: {email['subject']}
Body: {email['body']}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful email assistant."
        ),
        contents=prompt
    )
    return response.text

def send_reply(service, original_email, reply_text):
    """
    Send the generated reply to the sender
    """
    to_email = original_email.get('from', '')  
    subject = "Re: " + original_email['subject']

    message = MIMEText(reply_text)
    message['to'] = to_email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId='me',
        body={'raw': raw_message}
    ).execute()
    print(f"sent to {to_email}")

