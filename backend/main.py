from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
from openai import OpenAI

# Load .env file and OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env file")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class QuestionRequest(BaseModel):
    question: str

# Path to Q&A storage
QA_DATA_FILE = "qa_data.json"

# Append Q&A to file
def save_qa(question, answer):
    data = []
    if os.path.exists(QA_DATA_FILE):
        try:
            with open(QA_DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

    data.append({"question": question, "answer": answer})
    with open(QA_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Root endpoint (health check)
@app.get("/")
def read_root():
    return {"message": "University Info API is live."}

# Main endpoint
@app.post("/ask")
def ask_question(req: QuestionRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful university assistant. Only respond to questions related to "
                        "Portland State University (PSU) or Oregon State University (OSU) or University of Oregon (UO). "
                        "If the question is about another university or unrelated topic, reply: "
                        "'Sorry, I can only help with PSU, OSU and UO information.'"
                    )
                },
                {"role": "user", "content": req.question}
            ]
        )

        answer = response.choices[0].message.content.strip()
        save_qa(req.question, answer)
        return {"answer": answer}

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
