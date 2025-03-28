import re
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob

# Ensure stopwords are downloaded
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def clean_text(text):
    """
    Cleans text by removing special characters, URLs, and stopwords.
    
    Args:
        text (str): The raw text.
    
    Returns:
        str: Cleaned text.
    """
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    text = " ".join(word for word in text.split() if word not in stop_words)  # Remove stopwords
    return text

def analyze_sentiment(text):
    """
    Performs sentiment analysis using TextBlob.
    
    Args:
        text (str): The cleaned text.
    
    Returns:
        dict: Sentiment label and polarity score.
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {"sentiment": sentiment, "polarity": round(polarity, 2)}

def preprocess_articles(articles):
    """
    Preprocesses a list of news articles and extracts sentiment.
    
    Args:
        articles (list): List of news articles (each as a dictionary).
    
    Returns:
        list: List of dictionaries with cleaned text and sentiment.
    """
    processed_articles = []
    for article in articles:
        cleaned_text = clean_text(article["title"] + " " + article.get("description", ""))
        sentiment_result = analyze_sentiment(cleaned_text)

        processed_articles.append({
            "title": article["title"],
            "cleaned_text": cleaned_text,
            "sentiment": sentiment_result["sentiment"],
            "polarity": sentiment_result["polarity"],
            "url": article["url"]
        })

    return processed_articles

# Test function
if __name__ == "__main__":
    from scraper import fetch_news
    test_articles = fetch_news("Apple")
    processed_data = preprocess_articles(test_articles)
    for data in processed_data[:5]:  # Show first 5 processed articles
        print(data)
