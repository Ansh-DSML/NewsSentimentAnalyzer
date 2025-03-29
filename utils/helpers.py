import re
import numpy as np

def clean_text(text: str) -> str:
    """Removes special characters, multiple spaces, and converts text to lowercase."""
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text.lower()

def sentiment_score(predictions: list) -> str:
    """Returns sentiment label based on model predictions."""
    score = np.mean(predictions)
    if score > 0.5:
        return "Positive"
    elif score < -0.5:
        return "Negative"
    return "Neutral"

def extract_keywords(text: str, top_n=5) -> list:
    """Extracts top N keywords from text based on frequency."""
    words = text.split()
    word_freq = {word: words.count(word) for word in set(words)}
    sorted_words = sorted(word_freq, key=word_freq.get, reverse=True)
    return sorted_words[:top_n]