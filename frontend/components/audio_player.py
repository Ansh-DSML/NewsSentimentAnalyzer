import streamlit as st
import base64
import os

def audio_player(audio_path):
    """Embeds an audio player for Hindi text-to-speech output."""
    if not os.path.exists(audio_path):
        st.warning(f"⚠️ Audio file not found: {audio_path}")
        return
    
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        audio_tag = f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
        st.markdown(audio_tag, unsafe_allow_html=True)
