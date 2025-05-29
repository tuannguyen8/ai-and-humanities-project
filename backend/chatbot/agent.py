import json

with open("data/knowledge_base.json", "r") as f:
    knowledge = json.load(f)

def get_bot_response(message: str) -> str:
    message = message.lower()
    for category, info in knowledge.items():
        if category.lower() in message:
            return info
    return "Sorry, I couldn't find information related to your query."
