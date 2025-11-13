
import os, base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.config import GOOGLE_API_SCOPES

class GoogleClient:
    creds = None
    token_file = None
    email_client = None
    chat_client = None
    
    def __init__(self, token_file):
        self.token_file = token_file
        self.authenticate()
        
    def authenticate(self):
        if not self.token_file:
            self.token_file = "token.json"
            
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", GOOGLE_API_SCOPES)

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", GOOGLE_API_SCOPES)
            try:
                creds = flow.run_local_server(port=0, prompt='consent')
            except:
                creds = flow.run_console(prompt='consent')
            with open("token.json", "w") as f:
                f.write(creds.to_json())
            print("token.json created successfully!")

        self.creds = creds
        self.email_client = build('gmail', 'v1', credentials=creds)
        self.chat_client = build('chat', 'v1', credentials=creds)
    
    def email(self):
        return self.email_client
    
    def chat(self):
        return self.chat_client