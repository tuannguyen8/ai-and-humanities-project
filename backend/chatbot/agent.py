import json

def load_knowledge_base():
    with open("data/knowledge_base.json", "r", encoding="utf-8") as file:
        return json.load(file)

kb = load_knowledge_base()

def get_response_from_knowledge(question: str) -> str:
    for item in kb:
        if any(word.lower() in item["question"].lower() for word in question.split()):
            return item["answer"]
    return "Sorry, I don't have an answer for that question."
