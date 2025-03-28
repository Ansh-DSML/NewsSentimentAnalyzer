import streamlit as st
import requests
import uvicorn
from threading import Thread
from fastapi import FastAPI

# Import local components
from components.input_form import input_form
from components.display_results import display_results
from components.audio_player import audio_player

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"

# FastAPI backend
app = FastAPI()

def fetch_sentiment_analysis(company_name):
    """Fetch sentiment analysis from backend API."""
    try:
        response = requests.post(f"{BACKEND_URL}/analyze", json={"company": company_name})
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Error: {e}")
        return None

def main():
    st.title("News Sentiment Analyzer")

    # Company name input from sidebar
    company_name, analyze_button = input_form()

    # Analysis for company
    if analyze_button and company_name:
        with st.spinner('Analyzing sentiment...'):
            result = fetch_sentiment_analysis(company_name)
            
            if result:
                # Extract sentiment and topics
                sentiment = result.get("sentiment", "Neutral")
                topics = result.get("topics", [])

                # Display results
                display_results(sentiment, topics)

                # Placeholder for audio summary
                audio_file = "output/hindi_summary.mp3"
                audio_player(audio_file)
            else:
                st.error("Error fetching sentiment analysis. Please try again.")

    # Text-based analysis
    user_input = st.text_area("Or Enter news article or text:")
    if st.button("Analyze Text Sentiment"):
        if user_input:
            try:
                response = requests.post(f"{BACKEND_URL}/analyze", json={"text": user_input})
                response.raise_for_status()
                result = response.json()
                
                sentiment = result.get("sentiment", "Neutral")
                topics = result.get("topics", [])
                
                display_results(sentiment, topics)
            except requests.exceptions.RequestException as e:
                st.error(f"Error analyzing text: {e}")

if __name__ == "__main__":
    main()