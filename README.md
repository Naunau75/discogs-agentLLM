# Music Information Retrieval API

## Overview

This project is a FastAPI-based web service that combines natural language processing with music database querying to provide detailed answers to music-related questions. It utilizes Claude AI for question analysis and response generation, and the Discogs API for retrieving music information.

## Features

- Natural language question processing
- Music information extraction from questions
- Discogs database querying
- AI-powered response generation
- Confidence scoring for answers

## Prerequisites

- Python 3.8+
- FastAPI
- Anthropic API key
- Discogs API key and secret

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/music-info-retrieval-api.git
   cd music-info-retrieval-api
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   DISCOGS_API_KEY=your_discogs_api_key
   DISCOGS_API_SECRET=your_discogs_api_secret
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn backend.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. Use the `/ask` endpoint to submit questions:
   ```
   POST /ask
   {
     "text": "Who released the album 'Thriller' in 1982?"
   }
   ```

## API Endpoints

### POST /ask

Submit a music-related question.

Request body:

json
{
"answer": "string",
"confidence": "float",
"discogs_info": {
"artist": "string",
"title": "string",
"year": "integer",
"genre": "string"
}
}

## Architecture

1. Question Analysis: The input question is processed by Claude AI to extract relevant music information.
2. Discogs Query: The extracted information is used to query the Discogs database.
3. Response Generation: Claude AI generates a final response based on the original question and Discogs data.
4. Confidence Scoring: A confidence score is assigned based on the quality of the Discogs results.

## Error Handling

The API uses extensive logging to track the flow of execution and capture any errors. Errors are logged and appropriate HTTP exceptions are raised with descriptive messages.