from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request format must now include both question and reply
class ChatEntry(BaseModel):
    question: str
    reply: str

# Save interaction to file
def save_interaction(entry: ChatEntry, file_path="questions.json"):
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
    data.append(entry.dict())
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# POST endpoint to receive question + reply
@app.post("/chat")
async def chat(entry: ChatEntry):
    save_interaction(entry)
    return {"status": "saved"}
