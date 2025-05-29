from fastapi import FastAPI, Request
from models.schema import ChatRequest, ChatResponse
from chatbot.agent import get_bot_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = get_bot_response(request.message)
    return ChatResponse(reply=reply)
