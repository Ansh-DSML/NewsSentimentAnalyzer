import os
from gtts import gTTS
from googletrans import Translator  # ✅ Better translation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get backend path
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "output", "hindi_summary.mp3")  # Absolute path

def text_to_speech(text, lang="hi", output_file=OUTPUT_PATH):
    """Translates text to Hindi and converts it to speech."""
    if not text.strip():
        print("Error: No text provided for speech synthesis.")
        return None

    try:
        # ✅ Use googletrans for better translation
        translator = Translator()
        translated_text = translator.translate(text, src="en", dest="hi").text

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        tts = gTTS(text=translated_text, lang=lang, slow=False)
        tts.save(output_file)

        if os.path.exists(output_file):
            return output_file
        else:
            print("Error: Failed to generate audio file.")
            return None
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

def generate_audio(text: str) -> str:
    """Wrapper function to call text_to_speech and return the audio path."""
    return text_to_speech(text, lang="hi", output_file=OUTPUT_PATH)
