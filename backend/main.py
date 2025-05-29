from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schema import Question, ChatResponse
import json, os
from datetime import datetime
import openai

# Set your OpenAI API key here
openai.api_key = " "

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "storage/questions.json"

@app.post("/submit", response_model=ChatResponse)
async def submit_question(question: Question):
    user_message = question.message

    # Call OpenAI GPT model to get a smart answer
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful university assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        answer = completion['choices'][0]['message']['content'].strip()
    except Exception as e:
        answer = f"Error getting response from LLM: {str(e)}"

    # Save question and answer
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": user_message,
        "answer": answer
    }

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    data.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {"reply": answer}
