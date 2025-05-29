from pydantic import BaseModel

class Question(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
