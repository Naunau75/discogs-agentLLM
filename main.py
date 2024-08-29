from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import logging
from scrapfly import ScrapeConfig, ScrapflyClient
import instructor
from anthropic import Anthropic

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scrapfly = ScrapflyClient(key=os.getenv("SCRAPFLY_API_KEY"))
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# Remplacez la fonction get_claude_answer par celle-ci
async def get_claude_answer(question: str):
    client = instructor.from_anthropic(
        Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    )
    prompt = f"Voici une question sur Discogs : {question}\n\nRéponds à cette question en te basant sur tes connaissances sur Discogs. Fournis également un niveau de confiance pour ta réponse sur une échelle de 0 à 1."

    # Utiliser instructor.complete() au lieu de client.completions.create()
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_model=DiscogsAnswer,
    )

    return response


class Question(BaseModel):
    text: str


class DiscogsAnswer(BaseModel):
    answer: str
    confidence: float


@app.post("/ask")
async def ask_question(question: Question):
    logger.info(f"Question reçue : {question.text}")

    claude_answer = await get_claude_answer(question.text)
    discogs_results = await search_discogs(question.text)
    scraped_data = await scrape_discogs(discogs_results)

    return {
        "claude_answer": claude_answer.answer,
        "confidence": claude_answer.confidence,
        "discogs_results": discogs_results,
        "scraped_data": scraped_data,
    }


async def search_discogs(query: str):
    discogs_api_key = os.getenv("DISCOGS_API_KEY")
    discogs_api_secret = os.getenv("DISCOGS_API_SECRET")
    headers = {
        "User-Agent": "VotreAppDiscogs/1.0",
        "Authorization": f"Discogs key={discogs_api_key}, secret={discogs_api_secret}",
    }
    async with httpx.AsyncClient() as client:
        response = client.get(
            "https://api.discogs.com/database/search",
            params={"q": query, "type": "release"},
            headers=headers,
        )
        response.raise_for_status()
    return response.json()["results"][:5]


async def scrape_discogs(results):
    scrape_configs = [
        ScrapeConfig(
            url=f"https://www.discogs.com{result['uri']}", asp=True, country="US"
        )
        for result in results
        if "uri" in result
    ]
    scraped_data = await scrapfly.concurrent_scrape(scrape_configs)
    return [result.content for result in scraped_data]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
