from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx
import logging
import os
from dotenv import load_dotenv
from anthropic import Anthropic
import instructor

load_dotenv()


# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class Question(BaseModel):
    text: str


class DiscogsInfo(BaseModel):
    artist: Optional[str] = None
    title: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None


class QuestionAnswer(BaseModel):
    answer: str


class Response(BaseModel):
    answer: str
    confidence: float
    discogs_info: DiscogsInfo


@app.post("/ask")
async def ask_question(question: Question):
    try:
        # Analyser la question avec Claude
        client = instructor.from_anthropic(
            Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        )
        claude_response = client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[
                {
                    "role": "system",
                    "content": "Extrayez les informations musicales pertinentes de la question suivante.",
                },
                {"role": "user", "content": question.text},
            ],
            max_tokens=300,
            response_model=DiscogsInfo,
        )

        # Rechercher sur Discogs
        discogs_api_key = os.getenv("DISCOGS_API_KEY")
        discogs_api_secret = os.getenv("DISCOGS_API_SECRET")

        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(
                "https://api.discogs.com/database/search",
                params={
                    "q": f"{claude_response.artist} {claude_response.title} {claude_response.year} {claude_response.genre}",
                    "type": "release",
                    "key": discogs_api_key,
                    "secret": discogs_api_secret,
                },
                headers={
                    "User-Agent": "VotreAppName/1.0 +http://votresite.com",
                },
            )
            discogs_data = response.json()

        # Générer la réponse finale avec Claude
        final_response = client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[
                {
                    "role": "system",
                    "content": "Répondez à la question en utilisant les informations de Discogs.",
                },
                {
                    "role": "user",
                    "content": f"Question: {question.text}\nDonnées Discogs: {discogs_data}",
                },
            ],
            max_tokens=4096,
            response_model=QuestionAnswer,
        )

        confidence = 0.8 if discogs_data["results"] else 0.5

        return Response(
            answer=final_response.answer,
            confidence=confidence,
            discogs_info=claude_response,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
