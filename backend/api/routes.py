from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentiment_analysis.sentiment_model import analyze_sentiment
from sentiment_analysis.topic_extraction import extract_topics
from backend.data_extraction.scraper import fetch_news
from data_extraction.preprocess import preprocess_articles

router = APIRouter()

class AnalysisRequest(BaseModel):
    company: str = None
    text: str = None

@router.post("/analyze")
def analyze(request: AnalysisRequest):
    try:
        if request.company:
            # Fetch and analyze news for a company
            articles = fetch_news(request.company)
            processed_articles = preprocess_articles(articles)
            
            # Extract topics from processed articles
            texts = [article['cleaned_text'] for article in processed_articles]
            topics = extract_topics(texts)
            
            # Determine overall sentiment
            sentiments = [article['sentiment'] for article in processed_articles]
            overall_sentiment = max(set(sentiments), key=sentiments.count)
            
            return {
                "company": request.company,
                "sentiment": overall_sentiment,
                "topics": topics
            }
        
        elif request.text:
            # Analyze sentiment of provided text
            sentiment_result = analyze_sentiment(request.text)
            topics = extract_topics([request.text])
            
            return {
                "sentiment": sentiment_result['sentiment'],
                "topics": topics
            }
        
        else:
            raise HTTPException(status_code=400, detail="No input provided")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))