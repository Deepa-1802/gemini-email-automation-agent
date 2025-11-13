import os
import json
import requests
from src.classifier import classify_email, update_gmail_label
from src.gmail_fetcher import fetch_emails
from src.responder_llm import generate_reply, send_reply

class BaseAgent:
    def run(self, input_data):
        raise NotImplementedError
    
class FetchEmailAgent(BaseAgent):
    def __init__(self, email_client):
        super().__init__()
        self.email_client = email_client

    def run(self, _):
        try:
            emails = fetch_emails(self.email_client)
            if emails:
                top_email = emails[0]
                self.email_client.users().messages().modify(
                    userId="me",
                    id=top_email['id'],
                    body={"removeLabelIds": ["UNREAD"]}
                ).execute()

                print(f"New email fetched: {top_email['subject']}")
                return top_email
            return None
        except Exception as e:
            print(f"FetchEmailAgent Error: {e}")
            return None
        
class ClassifierAgent(BaseAgent):
    def run(self, email):
        if not email or "subject" not in email:
            return None
        try:
            category = classify_email(email)
            email["category"] = category
            print(f"Classified as: {category}")
            return email
        except Exception as e:
            print(f"ClassifierAgent Error: {e}")
            return email

class PriorityAgent(BaseAgent):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url

    def run(self, email):
        if not email:
            return None

        try:
            category = email.get("category")
            if category == "urgent":
                # Generate a short suggested reply 
                suggested_reply = generate_reply(email, category)

                message = (
                    f"* Urgent Email Received!* \n"
                    f"**From:** {email.get('from', 'Unknown')}\n"
                    f"**Subject:** {email.get('subject', 'No Subject')}\n"
                    f"**Snippet:** {email.get('body', '')[:200]}...\n\n"
                    f"**Suggested Reply:**\n{suggested_reply}"
                )

                payload = {"text": message}

                # Send notification to Google Chat 
                response = requests.post(self.webhook_url, json=payload)

                if response.status_code == 200:
                    print("Urgent email notification sent to Google Chat.")
                else:
                    print(f"Failed to send message to Chat: {response.text}")

            return email

        except Exception as e:
            print(f"PriorityAgent Error: {e}")
            return email

class ResponderAgent(BaseAgent):
    def __init__(self, email_client):
        super().__init__()
        self.email_client = email_client

    def run(self, email):
        if not email or "subject" not in email:
            return None
        try:
            reply_text = generate_reply(email, email.get("category", "work"))
            send_reply(self.email_client, email, reply_text)
            update_gmail_label(self.email_client, email["id"], email.get("category", "work"))
            print(f"ResponderAgent: Email processed and replied → {email['subject']}")
            
            #Update the cache 
            cache_file = "processed_cache.json"
            processed = set()
            if os.path.exists(cache_file):
                with open(cache_file, "r") as f:
                    processed = set(json.load(f))
            processed.add(email["id"])
            with open(cache_file, "w") as f:
                json.dump(list(processed), f, indent=2)

            # Mark the email as read immediately
            self.email_client.users().messages().modify(
                userId="me",
                id=email["id"],
                body={"removeLabelIds": ["UNREAD"]}
            ).execute()
            return email
        except Exception as e:
            print(f" ResponderAgent Error: {e}")
            return email
