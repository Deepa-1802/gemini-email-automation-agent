from clients.gemini_client import client
from google.genai import types
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import os

def classify_email(email):
    prompt = f"""
    Classify this email into one of: urgent, personal, work, spam.
    Subject: {email['subject']}
    Body: {email['body']}
    Only return the category.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are an email classification assistant."
        ),
        contents=prompt
    )
    category = response.text.strip().lower()
    return category

def get_latest_unread_email(service):
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX', 'UNREAD'],
        maxResults=1
    ).execute()
    messages = results.get('messages', [])
    if not messages:
        return None
    return messages[0]['id']

def get_email_content(service, message_id):
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    headers = message['payload']['headers']
    subject = next(h['value'] for h in headers if h['name'] == 'Subject')

    # Decode email body
    body = ""
    parts = message['payload'].get('parts', [])
    if parts:
        body_data = parts[0]['body'].get('data', '')
        if body_data:
            body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
    else:
        body_data = message['payload']['body'].get('data', '')
        if body_data:
            body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')

    return {'id': message_id, 'subject': subject, 'body': body}

def update_gmail_label(service, message_id, category):
    try:
        label_name = category.capitalize()
        labels = service.users().labels().list(userId="me").execute().get("labels", [])
        label_id = next((lbl["id"] for lbl in labels if lbl["name"].lower() == label_name.lower()), None)
        if not label_id:
            new_label = {
                "name": label_name,
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show",
            }
            created_label = service.users().labels().create(userId="me", body=new_label).execute()
            label_id = created_label["id"]
            print(f" Created new Gmail label: {label_name}")

        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"addLabelIds": [label_id], "removeLabelIds": []},
        ).execute()
        print(f"Email labeled as: {label_name}")

    except Exception as e:
        print(f" update_gmail_label Error: {e}")
