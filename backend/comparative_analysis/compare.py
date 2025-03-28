import requests
from textblob import TextBlob
from datetime import datetime, timedelta
import config

NEWS_API_KEY = config.NEWS_API_KEY
NEWS_API_URL = "https://newsapi.org/v2/everything"


def fetch_news(company, from_date, to_date):
    """Fetch news articles for a given company within a date range."""
    params = {
        "q": company,
        "from": from_date,
        "to": to_date,
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []


def analyze_sentiment(text):
    """Analyze sentiment using TextBlob."""
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # Ranges from -1 (negative) to 1 (positive)
    return sentiment_score


def compare_companies(companies):
    """Compare sentiment analysis of multiple companies."""
    to_date = datetime.today().strftime("%Y-%m-%d")
    from_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

    sentiment_results = {}

    for company in companies:
        articles = fetch_news(company, from_date, to_date)
        total_sentiment = 0
        count = 0

        for article in articles:
            sentiment = analyze_sentiment(article["title"] + " " + article.get("description", ""))
            total_sentiment += sentiment
            count += 1

        avg_sentiment = total_sentiment / count if count > 0 else 0
        sentiment_results[company] = avg_sentiment

    return sentiment_results


if __name__ == "__main__":
    companies = ["Google", "Microsoft", "Apple", "Amazon", "Meta"]
    results = compare_companies(companies)
    print(results)
