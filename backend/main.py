from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Create FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QuestionRequest(BaseModel):
    question: str

# Only allow PSU, ASU, and UO
ALLOWED_KEYWORDS = [
    "portland state", "psu",
    "arizona state", "asu",
    "university of oregon", "uo"
]

# Function to fetch answer from OpenAI
def get_openai_response(prompt: str) -> str:
    if not any(kw in prompt.lower() for kw in ALLOWED_KEYWORDS):
        return "Sorry, I can only help with Portland State University (PSU), Arizona State University (ASU), and University of Oregon (UO)."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an academic assistant that only provides information about PSU, ASU, and UO."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API error: {e}"

# API endpoint
@app.post("/ask")
async def ask_question(req: QuestionRequest):
    question = req.question.strip()
    answer = get_openai_response(question)

    # Save to qa_data.json
    try:
        path = os.path.join(os.path.dirname(__file__), "qa_data.json")
        data = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

        data.append({"question": question, "answer": answer})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"Error writing to file: {e}")

    return {"answer": answer}

# Default health route
@app.get("/")
def root():
    return {"message": "University Assistant API is live."}
