from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    text: str


@app.post("/ask")
async def ask_question(question: Question):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }

    payload = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "Vous êtes un assistant spécialisé dans les informations sur Discogs.",
            },
            {"role": "user", "content": question.text},
        ],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages", json=payload, headers=headers
        )

    if response.status_code == 200:
        return {"answer": response.json()["content"][0]["text"]}
    else:
        return {"error": "Erreur lors de la communication avec Claude"}
