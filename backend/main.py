from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schema import ChatRequest, ChatResponse
from chatbot.agent import get_response_from_knowledge
from chatbot.logger import log_conversation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = get_response_from_knowledge(request.question)
    log_conversation(request.question, answer)
    return ChatResponse(answer=answer)
