📧 Automated Email Responder Agent
🧠 Overview

The AI Email Responder Agent automates Gmail inbox management by classifying, labeling, and replying to incoming emails. It uses Gemini API for intelligent email classification, LangGraph to orchestrate the agent workflow, and Google Chat Webhooks for urgent email alerts.

The system operates in a continuous loop — fetching new emails, classifying them into categories (Work, Personal, Spam, or Urgent), applying Gmail labels, generating AI-powered replies, and notifying urgent messages in Google Chat.

⚙️ Features

✅ Email Fetching — Reads new emails using Gmail API
✅ Classification (Gemini API) — Categorizes emails as Work, Personal, Spam, or Urgent
✅ Auto Labeling — Adds labels inside Gmail automatically
✅ Smart Reply Generation — Generates a polite and concise response
✅ Priority Alerts — Urgent emails are pushed to a Google Chat Space via webhook
✅ Continuous Workflow — Runs in background with periodic checks using asyncio
✅ Modular Design — Each step is handled by a separate agent (fetcher, classifier, responder, priority handler)

🧩 Project Structure

📂 project-root/
│
├── clients/
│   ├── gemini_client.py       # Handles Gemini API calls for classification
│   └── google_client.py       # Gmail & Chat API integration
│
├── src/
│   ├── agents.py              # All agent classes (fetch, classify, priority, respond)
│   ├── classifier.py          # Gemini-based email classifier
│   ├── gmail_fetcher.py       # Fetches unread emails from Gmail
│   ├── orchestrator.py        # Workflow logic for labeling and reply
│   ├── responder_llm.py       # Generates LLM-based replies
│   └── config.py              # Environment variable and token configuration
│
├── main.py                    # LangGraph workflow entrypoint
├── credentials.json           # Google API credentials
├── token.json                 # OAuth token file for Gmail API
├── processed_cache.json       # Cache to track processed emails
├── requirements.txt           # Python dependencies
├── .env                       # API keys and webhook URL
├── .gitignore
└── README.md


🧰 Tech Stack

Python 3.10+

Gemini API: Text classification & response generation

LangGraph: Workflow orchestration

Google Gmail API

Google Chat Webhooks

Asyncio: Background email polling

🧪 Installation

1️⃣ Clone this repository

git clone https://github.com/deepa-1802/ai-email-responder.git 
cd ai-email-responder

2️⃣ Create virtual environment

python -m venv venv
venv\Scripts\activate  # On Windows

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Add your environment variables

Create a .env file in the project root:

# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Google Webhook (for urgent email alerts)
GOOGLE_CHAT_WEBHOOK=https://chat.googleapis.com/v1/spaces/...


5️⃣ Run the workflow
python main.py

🧠 Workflow Overvie

| Step | Agent             | Function                                      |
| ---- | ----------------- | --------------------------------------------- |
| 1️⃣  | `FetchEmailAgent` | Pulls unread emails from Gmail                |
| 2️⃣  | `ClassifierAgent` | Uses Gemini to classify each email            |
| 3️⃣  | `PriorityAgent`   | Sends urgent email details to Google Chat     |
| 4️⃣  | `ResponderAgent`  | Generates and stores AI reply in Gmail Drafts |
| 5️⃣  | `Orchestrator`    | Handles labeling and process flow             |


🪶 Example Output

When an urgent email is detected:

*Urgent Email Received!*
From: john@company.com
Subject: Server Down Alert
Snippet: The production server is currently down and needs immediate attention.
Suggested Reply:
"Thank you for the alert. We’re looking into this issue and will provide an update shortly."


A Gmail label “Urgent” is applied, and the same message is sent to Google Chat.