from gtts import gTTS
import os

def text_to_speech(text, lang="hi", output_file="output/hindi_summary.mp3"):
    """
    Converts text to speech and saves the audio file.

    Args:
        text (str): The text to be converted to speech.
        lang (str): Language for speech synthesis (default: Hindi 'hi').
        output_file (str): Path to save the generated audio file.
    
    Returns:
        str: Path to the generated audio file or None if an error occurs.
    """
    if not text.strip():
        print("Error: No text provided for speech synthesis.")
        return None

    try:
        # ✅ Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        # ✅ Generate speech
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)

        # ✅ Check if file was created successfully
        if os.path.exists(output_file):
            return output_file
        else:
            print("Error: Failed to generate audio file.")
            return None
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None
