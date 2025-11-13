from src.gmail_fetcher import fetch_emails
from src.classifier import classify_email
from src.responder_llm import generate_reply

def run_pipeline():
    emails = fetch_emails()
    results = []
    for email in emails:
        category = classify_email(email)
        reply = generate_reply(email, category)
        results.append({
            "id": email['id'],
            "subject": email['subject'],
            "category": category,
            "reply": reply
        })
    print(results)
    return results
