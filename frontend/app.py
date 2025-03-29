import streamlit as st
import requests
from components.input_form import input_form
from components.display_results import display_results
from components.audio_player import audio_player

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"

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
                # Display full analysis results
                st.subheader("Sentiment Analysis Result")
                st.write(f"**Company:** {result.get('Company', 'N/A')}")

                # Display Articles
                st.subheader("News Articles Analyzed")
                for article in result.get("Articles", []):
                    st.markdown(f"**Title:** {article['Title']}")
                    st.markdown(f"**Summary:** {article['Summary']}")
                    st.markdown(f"**Sentiment:** {article['Sentiment']}")
                    st.markdown(f"**Topics:** {', '.join(article['Topics'])}")
                    st.write("---")

                # Display Comparative Sentiment Score
                st.subheader("Comparative Sentiment Score")
                sentiment_distribution = result.get("Comparative Sentiment Score", {}).get("Sentiment Distribution", {})
                st.json(sentiment_distribution)

                coverage_differences = result.get("Comparative Sentiment Score", {}).get("Coverage Differences", [])
                for diff in coverage_differences:
                    st.markdown(f"**Comparison:** {diff['Comparison']}")
                    st.markdown(f"**Impact:** {diff['Impact']}")
                    st.write("---")

                topic_overlap = result.get("Comparative Sentiment Score", {}).get("Topic Overlap", {})
                st.subheader("Topic Overlap")
                st.json(topic_overlap)

                # Final Summary
                st.subheader("Final Sentiment Analysis")
                final_summary = result.get("Final Sentiment Analysis", "N/A")
                st.markdown(final_summary)

                # Generate and play audio summary
                with st.spinner("Generating audio summary..."):
                    audio_response = requests.post(f"{BACKEND_URL}/generate_audio", json={"text": final_summary})
    
                    if audio_response.status_code == 200:
                        audio_data = audio_response.json()
                        if "audio_path" in audio_data:
                            st.subheader("Audio Summary")
                            audio_player(f"{BACKEND_URL}/get_audio")  # ✅ Use FastAPI's endpoint
                        else:
                            st.error("Audio generation failed.")
                    else:
                        st.error("Failed to generate audio.")

if __name__ == "__main__":
    main()
