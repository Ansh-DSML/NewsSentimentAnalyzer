import nltk
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

# Download necessary NLTK data
nltk.download("vader_lexicon")

# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Performs sentiment analysis using both TextBlob and VADER.

    Args:
        text (str): The cleaned text.

    Returns:
        dict: Sentiment label, polarity, and confidence score.
    """
    if not text.strip():
        return {"sentiment": "Neutral", "polarity": 0.0, "confidence": 0.0}

    # TextBlob Polarity
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Scale: -1 (Negative) to 1 (Positive)

    # VADER Sentiment Score
    vader_scores = sia.polarity_scores(text)
    compound_score = vader_scores["compound"]  # Overall sentiment score

    # Determine final sentiment label
    if compound_score >= 0.05:
        sentiment = "Positive"
    elif compound_score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    confidence = round(abs(compound_score), 2)  # Confidence based on absolute score

    return {
        "sentiment": sentiment,
        "polarity": round(polarity, 2),
        "confidence": confidence,
    }

# Test function
if __name__ == "__main__":
    test_text = "The company's stock surged after a great earnings report!"
    result = analyze_sentiment(test_text)
    print(result)
