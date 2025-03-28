from fastapi import APIRouter, Query
import requests
from textblob import TextBlob
from datetime import datetime, timedelta

router = APIRouter()

# Your NewsAPI key
NEWS_API_KEY = "5eab13d77b3148d99f8b19b7efd9502b"
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(company_name: str):
    """Fetches news articles from the last 7 days for a given company."""
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

    params = {
        "q": company_name,
        "from": start_date,
        "to": end_date,
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        return []

def analyze_sentiment(text):
    """Performs sentiment analysis on a given text using TextBlob."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {"sentiment": sentiment, "polarity": polarity}

@router.get("/analyze")
def analyze(company: str = Query(..., title="Company Name", description="Name of the company to analyze")):
    """Fetches news articles for a company and analyzes sentiment."""
    articles = fetch_news(company)
    if not articles:
        return {"error": "No articles found"}

    results = []
    for article in articles[:10]:  # Limit to 10 articles for efficiency
        title = article.get("title", "")
        description = article.get("description", "")

        sentiment_result = analyze_sentiment(title + " " + description)

        results.append({
            "title": title,
            "description": description,
            "sentiment": sentiment_result["sentiment"],
            "polarity": sentiment_result["polarity"],
            "url": article.get("url", "")
        })

    return {"company": company, "articles_analyzed": len(results), "results": results}
