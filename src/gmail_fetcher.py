import os, base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email import message_from_bytes

def get_email_body(email_msg):
    if email_msg.is_multipart():
        for part in email_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='ignore')
        return ""
    else:
        payload = email_msg.get_payload(decode=True)
        if payload:
            return payload.decode('utf-8', errors='ignore')
        else:
            return ""

def fetch_emails(email_client):
    results = email_client.users().messages().list(userId='me', q='is:unread', maxResults=1).execute()
    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        m = email_client.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
        msg_bytes = base64.urlsafe_b64decode(m['raw'])
        email_msg = message_from_bytes(msg_bytes)

        from_header = email_msg.get('From', '')
        sender_email = from_header.split('<')[-1].replace('>', '').strip() if '<' in from_header else from_header.strip()

        emails.append({
            "id": msg['id'],
            "subject": email_msg['Subject'],
            "body": get_email_body(email_msg),
            "from": sender_email
        })

    print(emails)

    return emails

if __name__ == "__main__":
    emails = fetch_emails()
    print(emails)
