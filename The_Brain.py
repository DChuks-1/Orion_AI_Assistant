# The_Brain.py - OpenAI GPT Integration

import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def chat_with_openai(prompt, conversation_history=None):
    """Chat with OpenAI's GPT model"""
    if not OPENAI_API_KEY:
        return "Error: OpenAI API Key is missing. Please check your .env file."

    if conversation_history is None:
        conversation_history = []

    # Format conversation history for OpenAI
    messages = [{"role": "system", "content": "You are an intelligent AI assistant, similar to TARS and J.A.R.V.I.S"}]
    messages += conversation_history
    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use GPT-4o for best results
            messages=messages,
            temperature=0.7,
            max_tokens=512
        )

        # Extract AI response
        ai_response = response["choices"][0]["message"]["content"]

        # Update conversation history
        conversation_history.append({"role": "user", "content": prompt})
        conversation_history.append({"role": "assistant", "content": ai_response})

        # Keep history manageable (last 5 interactions)
        if len(conversation_history) > 5:
            conversation_history = conversation_history[-5:]

        return ai_response, conversation_history

    except Exception as e:
        return f"Error occurred: {str(e)}"
