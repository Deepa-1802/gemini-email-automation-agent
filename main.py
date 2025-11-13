import asyncio
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from src.agents import FetchEmailAgent, ClassifierAgent, PriorityAgent, ResponderAgent
from clients.google_client import GoogleClient

load_dotenv()
google_client = GoogleClient("token.json")
fetch_agent = FetchEmailAgent(google_client.email())
classifier_agent = ClassifierAgent()
chat_webhook_url = os.getenv("CHAT_WEBHOOK_URL")
priority_agent = PriorityAgent(chat_webhook_url)
responder_agent = ResponderAgent(google_client.email())

class EmailState(TypedDict, total=False):
    email: dict
    classification: str
    priority: str
    response: str

graph = StateGraph(EmailState)

graph.add_node("fetch", lambda state: {"email": fetch_agent.run(state)})
graph.add_node("classify", lambda state: {"email": classifier_agent.run(state["email"])})
graph.add_node("priority", lambda state: {"email": priority_agent.run(state["email"])})
graph.add_node("respond", lambda state: {"email": responder_agent.run(state["email"])})

graph.add_edge("fetch", "classify")
graph.add_edge("classify", "priority")
graph.add_edge("priority", "respond")

graph.set_entry_point("fetch")
graph.set_finish_point("respond")

workflow = graph.compile()

# Periodic check loop 
async def periodic_email_check():
    print("LangGraph Multi-Agent Email Responder running...")
    while True:
        print("Checking for new emails...")
        result = await workflow.ainvoke(EmailState())
        print("Workflow completed.")
        print(result)
        await asyncio.sleep(60)  

if __name__ == "__main__":
    asyncio.run(periodic_email_check())
