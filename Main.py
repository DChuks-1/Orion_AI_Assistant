# main.py - Main AI Assistant Program with OpenAI GPT Model

# Standard library imports
import speech_recognition as sr
import openai
import webbrowser
import wikipediaapi
import requests
import schedule
import time
import random
from dotenv import load_dotenv
import os

# Import functionality from your modular files
from The_Brain import chat_with_openai  # Ensure the file is correctly saved as The_Brain.py
from The_Voice import speak_elevenlabs

# Load OpenAI API Key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Track conversation history
conversation_history = []

def listen():
    """Capture audio and convert to text"""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening for your request...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            try:
                text = recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("Could not understand audio")
                return "I couldn't understand what you said."
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return "Sorry, I'm having trouble processing your speech right now."
    except OSError:
        print("No microphone detected. Please check your audio input.")
        return "No microphone found. Please type your command."

def search_wikipedia(query):
    """Fetch summary from Wikipedia using wikipediaapi"""
    wiki_wiki = wikipediaapi.Wikipedia('en')  # Initialize Wikipedia API
    page = wiki_wiki.page(query)

    if page.exists():
        return page.summary[:300]  # Return first 300 characters of summary
    else:
        return "No results found on Wikipedia."

def get_weather(city):
    """Fetch weather information"""
    api_key = os.getenv("WEATHER_API_KEY")  # Load API key from .env
    if not api_key:
        return "Weather API key is missing. Please configure your .env file."

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        response = requests.get(url).json()
        if 'current' in response:
            return f"Weather in {city}: {response['current']['condition']['text']}, {response['current']['temp_c']}°C."
        else:
            return "Could not fetch weather data. Please check the city name."
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

def open_website(query):
    """Open common websites"""
    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com",
        "stackoverflow": "https://stackoverflow.com"
    }
    if query in sites:
        webbrowser.open(sites[query])
        return f"Opening {query}..."
    return "Website not found."

def execute_command(command):
    """Process user command"""
    global conversation_history
    
    try:
        if "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            response = search_wikipedia(topic)
        elif "weather" in command:
            city = command.replace("weather", "").strip()
            response = get_weather(city)
        elif "open" in command:
            site = command.replace("open", "").strip()
            response = open_website(site)
        elif "reminder" in command:
            response = "Reminder feature not implemented yet!"
        else:
            # Use OpenAI GPT for general conversation
            response, conversation_history = chat_with_openai(command, conversation_history)

        print(f"Assistant: {response}")
        speak_elevenlabs(response)
    
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        speak_elevenlabs(error_msg)

# Task automation example
def remind_task():
    speak_elevenlabs("Reminder: Time to take a break!")

# Schedule reminder every hour
schedule.every().hour.do(remind_task)

if __name__ == "__main__":
    speak_elevenlabs("Hello! This is Orion, how can I help??")
    
    while True:
        user_input = listen()
        if user_input:
            if "exit" in user_input or "quit" in user_input:
                speak_elevenlabs("Goodbye!")
                break
            execute_command(user_input)

        # Run scheduled tasks
        schedule.run_pending()
        time.sleep(1)
