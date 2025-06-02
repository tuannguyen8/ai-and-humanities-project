from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from RAG.rag_agent import get_rag_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(q: Question):
    answer = get_rag_answer(q.message)
    return {"reply": answer}

@app.get("/")
def root():
    return {"message": "RAG Agent API is live."}