from fastapi import FastAPI
from pydantic import BaseModel
import streamlit as st
import requests
from components.input_form import input_form
from components.display_results import display_results
from components.audio_player import audio_player

# Get user input
company_name, analyze_button = input_form()

if analyze_button and company_name:
    # Mock sentiment and topics (Replace with actual API call)
    sentiment = "Positive"  # Example output
    topics = ["Stock Market", "New Product", "Investor Confidence"]

    display_results(sentiment, topics)

    # Play TTS audio summary
    audio_player("output/hindi_summary.mp3")

# Initialize FastAPI app
app = FastAPI()

# Define data model for input
class SentimentRequest(BaseModel):
    text: str

# Dummy sentiment analysis function
def analyze_sentiment(text):
    if "good" in text.lower():
        return {"sentiment": "positive", "confidence": 0.9}
    elif "bad" in text.lower():
        return {"sentiment": "negative", "confidence": 0.8}
    else:
        return {"sentiment": "neutral", "confidence": 0.7}

# Define FastAPI route
@app.post("/analyze")
def analyze(request: SentimentRequest):
    result = analyze_sentiment(request.text)
    return result

# Streamlit frontend
def main():
    st.title("News Sentiment Analyzer")
    user_input = st.text_area("Enter news article or text:")
    
    if st.button("Analyze Sentiment"):
        if user_input:
            response = requests.post("http://127.0.0.1:8000/analyze", json={"text": user_input})
            if response.status_code == 200:
                result = response.json()
                st.write(f"**Sentiment:** {result['sentiment']}")
                st.write(f"**Confidence:** {result['confidence']:.2f}")
            else:
                st.error("Error processing request.")
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    import uvicorn
    from threading import Thread
    
    # Run FastAPI backend in a separate thread
    backend_thread = Thread(target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000))
    backend_thread.daemon = True
    backend_thread.start()
    
    # Run Streamlit frontend
    main()
