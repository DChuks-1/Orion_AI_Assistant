# The_Voice.py - ElevenLabs TTS Integration

import requests
import os
import tempfile
from playsound import playsound
import pyttsx3  # Fallback TTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API keys from .env
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

def speak_elevenlabs(text):
    """Convert text to speech using ElevenLabs API"""
    
    # Check if API Key is set
    if not ELEVENLABS_API_KEY:
        print("Error: ElevenLabs API Key is missing. Falling back to pyttsx3.")
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return

    if not VOICE_ID:
        print("Error: ElevenLabs Voice ID is missing. Falling back to pyttsx3.")
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio.write(response.content)
                temp_audio_path = temp_audio.name

            playsound(temp_audio_path)
            os.unlink(temp_audio_path)

        else:
            print(f"ElevenLabs Error: {response.status_code}, {response.text}")
            # Fallback TTS
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

    except Exception as e:
        print(f"ElevenLabs TTS Error: {e}")
        # Fallback TTS
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
