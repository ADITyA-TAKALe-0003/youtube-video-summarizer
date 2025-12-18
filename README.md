# 🎥 YouTube Video Summarizer (AI Web App)

An AI-powered web application that summarizes YouTube videos by extracting audio, transcribing speech using Whisper, and generating structured summaries with a Large Language Model (Groq – Llama 3.1).

## 🚀 Features
- Summarizes YouTube videos into **Overview, Key Points, and Takeaways**
- Uses **Whisper** for speech-to-text (no captions required)
- Uses **Groq LLM (Llama 3.1)** for fast, high-quality summaries
- Handles multilingual transcripts
- Clean Streamlit UI with graceful error handling

## 🛠 Tech Stack
- Python
- Streamlit
- yt-dlp + FFmpeg
- faster-whisper
- Groq API (Llama 3.1)

## ⚙️ How It Works
1. User provides a YouTube video URL
2. Audio is extracted from the video
3. Whisper converts audio to text
4. Groq LLM generates a structured summary
5. Summary is displayed in the web interface

## ⚠️ Known Limitations
Due to YouTube restrictions on cloud-hosted environments, audio extraction may fail for some videos when deployed online.  
The application handles this gracefully by displaying clear error messages.

The app works reliably:
- When run locally
- For supported spoken-content videos (lectures, podcasts, tutorials)

## ▶️ Run Locally
```bash
git clone https://github.com/ADITyA-TAKALe-0003/youtube-video-summarizer
cd youtube-video-summarizer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
