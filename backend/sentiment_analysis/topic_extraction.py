import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

# Download NLTK stopwords
nltk.download("stopwords")
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    """
    Cleans and preprocesses text for topic extraction.
    
    Args:
        text (str): The raw text.
    
    Returns:
        str: Cleaned and processed text.
    """
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Remove URLs
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    text = " ".join(word for word in text.split() if word not in stop_words)  # Remove stopwords
    return text

def extract_topics(news_articles, num_topics=5):
    """
    Extracts key topics from a list of news articles using TF-IDF.

    Args:
        news_articles (list): List of cleaned text from news articles.
        num_topics (int): Number of top keywords to extract.

    Returns:
        list: List of top topics.
    """
    if not news_articles:
        return ["No topics found"]

    vectorizer = TfidfVectorizer(max_features=100, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(news_articles)
    feature_names = vectorizer.get_feature_names_out()

    # Get top words by frequency
    word_freq = Counter()
    for doc in tfidf_matrix.toarray():
        for i, freq in enumerate(doc):
            if freq > 0:
                word_freq[feature_names[i]] += freq

    top_keywords = [word for word, _ in word_freq.most_common(num_topics)]
    return top_keywords

# Test function
if __name__ == "__main__":
    sample_articles = [
        "Apple launches a new MacBook with AI features.",
        "Microsoft announces its latest cloud computing advancements.",
        "Tesla stock surges as new electric vehicle production expands.",
        "Google introduces a new AI chatbot for enterprise solutions.",
        "Amazon's revenue grows significantly in the latest quarter.",
    ]
    topics = extract_topics(sample_articles)
    print(f"Extracted Topics: {topics}")
