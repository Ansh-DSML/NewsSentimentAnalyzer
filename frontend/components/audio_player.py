import streamlit as st
import base64

def audio_player(audio_path):
    """Embeds an audio player for Hindi text-to-speech output."""
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        audio_tag = f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
        st.markdown(audio_tag, unsafe_allow_html=True)
