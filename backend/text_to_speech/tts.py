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
        str: Path to the generated audio file.
    """
    if not text.strip():
        print("Error: No text provided for speech synthesis.")
        return None

    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        return output_file
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

# Test function
if __name__ == "__main__":
    sample_text = "यह एक परीक्षण संदेश है।"
    audio_path = text_to_speech(sample_text)
    if audio_path:
        os.system(f"start {audio_path}")  # Play the generated audio file
