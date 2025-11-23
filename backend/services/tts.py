import os
from openai import OpenAI
from gtts import gTTS
import uuid
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_speech_google_cloud(text: str) -> str:
    """
    Convert text to speech using Google Cloud Text-to-Speech API.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    try:
        from google.cloud import texttospeech
        
        # Initialize client
        client_gcp = texttospeech.TextToSpeechClient()
        
        # Set the text input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-F",  # Female neural voice
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        # Select the audio config
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0
        )
        
        # Perform the text-to-speech request
        response = client_gcp.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Save the audio file
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(AUDIO_DIR, filename)
        
        with open(file_path, "wb") as out:
            out.write(response.audio_content)
        
        print("Google Cloud TTS: Audio content written successfully")
        return file_path
        
    except ImportError:
        print("Google Cloud TTS library not installed. Install with: pip install google-cloud-texttospeech")
        return None
    except Exception as e:
        print(f"Google Cloud TTS error: {e}")
        return None


def text_to_speech_azure(text: str) -> str:
    """
    Convert text to speech using Microsoft Azure Text-to-Speech API.
    Requires AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.
    """
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        # Get credentials from environment
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        service_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        
        if not speech_key:
            print("Azure Speech Key not found in environment variables")
            return None
        
        # Configure speech service
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=service_region
        )
        
        # Set voice (en-US-JennyNeural is a high-quality neural voice)
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        
        # Create audio config for file output
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(AUDIO_DIR, filename)
        audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
        
        # Create synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        # Synthesize speech
        result = speech_synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Azure TTS: Speech synthesized successfully")
            return file_path
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Azure TTS canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
            return None
            
    except ImportError:
        print("Azure Speech SDK not installed. Install with: pip install azure-cognitiveservices-speech")
        return None
    except Exception as e:
        print(f"Azure TTS error: {e}")
        return None


def text_to_speech_openai(text: str) -> str:
    """
    Convert text to speech using OpenAI TTS API.
    """
    try:
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(AUDIO_DIR, filename)
        
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        response.stream_to_file(file_path)
        print("OpenAI TTS: Audio generated successfully")
        return file_path
    except Exception as e:
        print(f"OpenAI TTS error: {e}")
        return None


def text_to_speech_gtts(text: str) -> str:
    """
    Convert text to speech using Google Text-to-Speech (gTTS) - Free offline option.
    """
    try:
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(AUDIO_DIR, filename)
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(file_path)
        print("gTTS: Audio generated successfully")
        return file_path
    except Exception as e:
        print(f"gTTS error: {e}")
        return None


def text_to_speech(text: str, preferred_service: str = "auto") -> str:
    """
    Converts text to speech and returns the file path.
    
    Args:
        text: The text to convert to speech
        preferred_service: Preferred TTS service - "openai", "google", "azure", "gtts", or "auto"
                          "auto" will try services in order based on availability
    
    Returns:
        File path to the generated audio file, or None if all methods fail
    """
    
    # Define service priority based on preference
    if preferred_service == "auto":
        # Try in order of quality: Azure -> Google Cloud -> OpenAI -> gTTS
        services = []
        
        # Check which services are available
        if os.getenv("AZURE_SPEECH_KEY"):
            services.append(("azure", text_to_speech_azure))
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            services.append(("google", text_to_speech_google_cloud))
        if os.getenv("OPENAI_API_KEY"):
            services.append(("openai", text_to_speech_openai))
        
        # Always add gTTS as fallback
        services.append(("gtts", text_to_speech_gtts))
        
    else:
        # Use specific service
        service_map = {
            "openai": text_to_speech_openai,
            "google": text_to_speech_google_cloud,
            "azure": text_to_speech_azure,
            "gtts": text_to_speech_gtts
        }
        
        if preferred_service in service_map:
            services = [(preferred_service, service_map[preferred_service])]
        else:
            print(f"Unknown service: {preferred_service}. Using auto mode.")
            return text_to_speech(text, "auto")
    
    # Try each service in order
    for service_name, service_func in services:
        print(f"Trying TTS service: {service_name}")
        result = service_func(text)
        if result:
            return result
        print(f"{service_name} TTS failed, trying next service...")
    
    print("All TTS services failed!")
    return None
