import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_text(transcript: str, summary_type: str = "short") -> str:
    """
    Sends transcript to Groq Llama 3 model and returns summary.
    summary_type = 'short', 'detailed', 'bullets'
    """
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not found. Add it to your .env file."

    prompt = ""

    if summary_type == "short":
        prompt = f"Summarize the following text in 5-6 lines:\n\n{transcript}"

    elif summary_type == "detailed":
        prompt = f"Write a detailed summary of this text:\n\n{transcript}"

    elif summary_type == "bullets":
        prompt = f"Give the key points from this text in bullet form:\n\n{transcript}"

    else:
        prompt = f"Summarize this text:\n\n{transcript}"

    url = "https://api.groq.com/openai/v1/chat/completions"

    payload = {
        "model": "llama3-8b-8192",  
        "messages": [
            {"role": "system", "content": "You are an expert summarizer."},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        return response_data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error during summarization: {str(e)}"
