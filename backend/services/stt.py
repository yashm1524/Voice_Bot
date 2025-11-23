import os
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path: str, use_whisper: bool = True) -> str:
    """
    Transcribes audio file to text.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"DEBUG: API Key present: {bool(api_key)}")
    if api_key:
        print(f"DEBUG: API Key starts with: {api_key[:8]}...")

    if use_whisper and api_key:
        print("DEBUG: Attempting Whisper transcription...")
        try:
            with open(file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            print("DEBUG: Whisper success")
            return transcription.text
        except Exception as e:
            print(f"Whisper error: {e}. Falling back to Google Speech Recognition.")
    
    print("DEBUG: Falling back to Google Speech Recognition")
    # Fallback to Google Speech Recognition
    recognizer = sr.Recognizer()
    try:
        # Attempt to convert to WAV using pydub if possible (requires ffmpeg usually, but worth a try)
        # If this fails, we proceed with the original file
        try:
            from pydub import AudioSegment
            print("DEBUG: Attempting audio conversion with pydub...")
            sound = AudioSegment.from_file(file_path)
            file_path = file_path + ".wav"
            sound.export(file_path, format="wav")
            print("DEBUG: Audio conversion successful")
        except Exception as conversion_error:
            print(f"DEBUG: Audio conversion failed (likely missing ffmpeg): {conversion_error}")

        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(f"DEBUG: Google STT result: {text}")
            return text
    except sr.UnknownValueError:
        print("DEBUG: Google STT: UnknownValueError")
        return "Could not understand audio"
    except sr.RequestError as e:
        print(f"DEBUG: Google STT RequestError: {e}")
        return f"Could not request results; {e}"
    except Exception as e:
        print(f"DEBUG: Google STT Generic Error: {e}")
        return f"Error processing audio: {e}"
