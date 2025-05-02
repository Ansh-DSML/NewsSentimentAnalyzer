from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
import json
import random
from text_to_speech.tts import generate_audio 
from text_to_speech.tts import text_to_speech 


app = FastAPI()

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "output","hindi_summary.mp3")

class AudioRequest(BaseModel):
    text: str


class CompanyRequest(BaseModel):
    company: str

def generate_mock_articles(company_name):
    """Generate multiple articles with diverse topics."""
    topics_list = [
        ["Stock Market", "Growth"],
        ["AI & Automation", "Workforce Changes"],
        ["Regulations", "Compliance Issues"],
        ["Partnerships", "New Contracts"],
        ["Financial Reports", "Revenue Growth"]
    ]

    articles = []
    for i in range(4):  # Generate 4 articles
        selected_topics = random.choice(topics_list)
        sentiment = random.choice(["Positive", "Negative", "Neutral"])
        articles.append({
            "Title": f"{company_name}'s Latest Update {i+1}",
            "Summary": f"Recent developments in {company_name} regarding {', '.join(selected_topics)}.",
            "Sentiment": sentiment,
            "Topics": selected_topics
        })
    
    return articles

@app.post("/analyze")
async def analyze(request: CompanyRequest):
    company_name = request.company

    # Generate multiple articles with diverse topics
    articles = generate_mock_articles(company_name)

    # Extract all unique topics
    unique_topics = list(set(topic for article in articles for topic in article["Topics"]))

    # Generate comparative sentiment analysis
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_counts[article["Sentiment"]] += 1

    # Intelligent Final Sentiment Analysis
    total_articles = len(articles)
    if sentiment_counts["Positive"] > sentiment_counts["Negative"] and sentiment_counts["Positive"] > sentiment_counts["Neutral"]:
        final_sentiment = f"{company_name} is experiencing **mostly positive** news coverage."
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"] and sentiment_counts["Negative"] > sentiment_counts["Neutral"]:
        final_sentiment = f"{company_name} is experiencing **mostly negative** news coverage."
    elif sentiment_counts["Neutral"] > sentiment_counts["Positive"] and sentiment_counts["Neutral"] > sentiment_counts["Negative"]:
        final_sentiment = f"{company_name} is experiencing **neutral** news coverage."
    else:
        final_sentiment = f"{company_name} has a **mixed sentiment** in recent news."

    response_data = {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_counts,
            "Topic Overlap": {
                "Common Topics": list(set.intersection(*map(set, [article["Topics"] for article in articles]))),
                "Unique Topics": unique_topics
            }
        },
        "Final Sentiment Analysis": final_sentiment
    }

    print("Response Sent to Frontend:", json.dumps(response_data, indent=4))  # Debugging
    return response_data

@app.post("/generate_audio")
async def generate_audio_endpoint(request: AudioRequest):
    audio_path = text_to_speech(request.text)  # Use correct function from tts.py
    if audio_path:
        return {"audio_path": "/get_audio"}  # Returning endpoint for Streamlit
    else:
        return {"error": "Audio generation failed"}

@app.get("/get_audio")
async def get_audio():
    if os.path.exists(OUTPUT_PATH):
        return FileResponse(OUTPUT_PATH, media_type="audio/mpeg", filename="hindi_summary.mp3")
    return {"error": "Audio file not found"}
