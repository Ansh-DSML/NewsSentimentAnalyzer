import streamlit as st

def audio_player(audio_url):
    """Play audio from backend API."""
    st.audio(audio_url, format="audio/mp3", start_time=0)
