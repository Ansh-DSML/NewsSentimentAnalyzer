import streamlit as st

def display_results(sentiment, topics):
    """Displays sentiment analysis and key topics."""
    st.subheader("Sentiment Analysis Result")

    sentiment_color = "green" if sentiment == "Positive" else "red" if sentiment == "Negative" else "gray"
    st.markdown(f"**Sentiment:** <span style='color:{sentiment_color}; font-weight:bold;'>{sentiment}</span>", unsafe_allow_html=True)

    st.subheader("Key Topics Identified")
    for topic in topics:
        st.markdown(f"- {topic}")

    st.success("Analysis Complete ✅")
