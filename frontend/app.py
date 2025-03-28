from fastapi import FastAPI
from pydantic import BaseModel
import streamlit as st
import requests
from components.input_form import input_form
from components.display_results import display_results
from components.audio_player import audio_player

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# Get user input from input_form
company_name, analyze_button = input_form()

if analyze_button and company_name:
    # Call the backend API to fetch news and analyze sentiment
    response = requests.post(f"{BACKEND_URL}/analyze", json={"company": company_name})

    if response.status_code == 200:
        result = response.json()
        
        # Extract sentiment and topics from API response
        sentiment = result.get("sentiment", "Neutral")
        topics = result.get("topics", [])

        # Display results using Streamlit components
        display_results(sentiment, topics)

        # Play TTS audio summary (if available)
        audio_file = "output/hindi_summary.mp3"  # This should be updated if dynamic
        audio_player(audio_file)
    else:
        st.error("Error fetching sentiment analysis. Please try again.")

# Initialize FastAPI app
app = FastAPI()

# Define data model for input
class SentimentRequest(BaseModel):
    company: str

# Define FastAPI route for sentiment analysis
@app.post("/analyze")
def analyze(request: SentimentRequest):
    """Calls the backend API to analyze sentiment for the given company."""
    response = requests.post(f"{BACKEND_URL}/api/analyze", json={"company": request.company})
    return response.json()

# Streamlit frontend
def main():
    st.title("News Sentiment Analyzer")

    user_input = st.text_area("Enter news article or text:")

    if st.button("Analyze Sentiment", key="text_analysis"):
        if user_input:
            response = requests.post(f"{BACKEND_URL}/api/analyze_text", json={"text": user_input})
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
