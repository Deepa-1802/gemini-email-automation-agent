# 📬 ***Automated Email Responder***
Smart. Seamless. Stress-free inbox management.

## 💡Overview

Managing email shouldn’t feel like a full-time job. The AI Email Responder Agent is a hands-free Gmail assistant that reads, classifies, and responds to emails intelligently and instantly.

Powered by Gemini API, LangGraph, and Google Chat Webhooks, this agent transforms your inbox into a self-organizing, self-responding system that’s always on and always accurate.


## What It Does

###  **- Real-Time Monitoring**
Continuously watches your Gmail inbox using asyncio, ensuring no   email is missed or processed twice.
###  **- Smart Classification**
Uses Gemini’s natural language understanding to sort emails into:    
   - Work

   - Personal

   - Spam

   - Urgent
###  **- Automated Actions**
  
  🏷️ Applies Gmail labels for clean organization

  💬 Generates polite, context-aware replies

  🚨 Sends urgent alerts to Google Chat for immediate attention


## Architecture Highlights

### **- LangGraph Workflow**
   Modular and event-driven, designed for scalability and maintainability.
### **- Asyncio Backbone**
   Enables continuous background execution without blocking or duplication.
### **-Google Chat Integration**
   Ensures urgent messages reach you instantly — even outside your inbox.


## Why It Matters

This isn’t just automation — it’s peace of mind. Whether you’re deep in work or offline for the weekend, your inbox stays organized, responsive, and alert-ready.

No more inbox anxiety. Just intelligent communication, handled quietly and efficiently.

## Features

 ***1.Email Fetching*** --             Reads new emails using Gmail API
 
 ***2.Classification (Gemini API)*** -- Categorizes emails as Work, Personal, Spam, or Urgent
 
 ***3.Auto Labeling*** --               Adds labels inside Gmail automatically
 
 ***4.Smart Reply Generation*** --       Generates a polite and concise response
 
 ***5.Priority Alerts*** --            Urgent emails are pushed to a Google Chat Space via webhook
 
 ***6.Continuous Workflow*** --        Runs in background with periodic checks using asyncio
 
 ***7.Modular Design*** --              Each step is handled by a separate agent (fetcher, classifier, responder, priority handler)




## Directory Structure

```plaintext

.
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
```


## Tech Stack

-  LangGraph: for developing AI agent Workflow 
-  Google Gmail API
-  Google Chat Webhooks
-  Asyncio: Background email polling


## Installation

## Prerequisites
 - Python 3.10+
 - Google Gemini api key (for embeddings)
 - Google Chat Webhooks
 - Gmail API credentials
 - Necessary Python libraries (listed in `requirements.txt`)

 
## setup

1. **Clone this repository**

```bash
git clone https://github.com/Deepa-1802/gemini-email-automation-agent.git
cd gemini-email-automation-agent
```
2. **Create virtual environment**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```
3. **Install dependencies**
   
```bash
pip install -r requirements.txt
```


## Configuration

The application requires several configuration settings (such as API keys and email server credentials). Create a `.env` file in the project root with the following variables:

```dotenv
# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Google Webhook (for urgent email alerts)
GOOGLE_CHAT_WEBHOOK=https://chat.googleapis.com/v1/spaces/...
```


## usage

To run the main email processing application, simply execute:

```bash
python main.py
```


## Workflow Overview


|Step| Agent             | Function                                      |
| ---| ----------------- | --------------------------------------------- |
| 1️  | `FetchEmailAgent` | Pulls unread emails from Gmail                |
| 2️  | `ClassifierAgent` | Uses Gemini to classify each email            |
| 3️  | `PriorityAgent`   | Sends urgent email details to Google Chat     |
| 4️  | `ResponderAgent`  | Generates and stores AI reply in Gmail Drafts |
| 5️  | `Orchestrator`    | Handles labeling and process flow             |




## Example Output

When an urgent email is detected:

```plaintext
*Urgent Email Received!*
From: john@company.com
Subject: Server Down Alert
Snippet: The production server is currently down and needs immediate attention.
Suggested Reply:
"Thank you for the alert. We’re looking into this issue and will provide an update shortly."
```


A Gmail label ```“Urgent”``` is applied, and the same message is sent to Google Chat.
