import streamlit as st
import os
import re
import yt_dlp
from faster_whisper import WhisperModel
from groq import Groq

# =========================
# CONFIG
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FILE = os.path.join(BASE_DIR, "audio.mp3")

# =========================
# Extract Video ID
# =========================
def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

# =========================
# Download Audio
# =========================
def download_audio(youtube_url):
    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": AUDIO_FILE.replace(".mp3", ".%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    if not os.path.exists(AUDIO_FILE):
        raise FileNotFoundError("Audio extraction failed.")

# =========================
# Whisper Transcription
# =========================
def transcribe_audio():
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(AUDIO_FILE)
    return " ".join(seg.text for seg in segments)

# =========================
# Groq Summarization
# =========================
def summarize_text(text):
    client = Groq(api_key=GROQ_API_KEY)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert multilingual video summarizer. "
                    "If the transcript is not in English, first translate it to English. "
                    "Then produce a clear, structured summary."
                )
            },
            {
                "role": "user",
                "content": f"""
Summarize the following YouTube video transcript using this structure:

### Overview
- 2–3 sentences explaining what the video is about

### Key Points
- Bullet points of the most important ideas

### Actionable Takeaways
- Practical insights or lessons for the viewer

Transcript:
{text}
"""
            }
        ],
        temperature=0.3,
        max_tokens=600
    )

    return completion.choices[0].message.content

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="YouTube Video Summarizer", layout="centered")

st.title("🎥 YouTube Video Summarizer (Whisper + Groq)")
st.info(
    "ℹ️ Best results for videos with **clear spoken audio** like podcasts, lectures, or tutorials.\n\n"
    "❌ Music-only videos, chants, or heavily edited clips may fail."
)

youtube_url = st.text_input("Enter YouTube Video URL")

if st.button("Summarize"):
    if not youtube_url:
        st.error("Please enter a YouTube URL.")
        st.stop()

    with st.spinner("⬇️ Downloading audio..."):
        try:
            download_audio(youtube_url)
        except Exception:
            st.error("❌ Failed to extract audio. Try a different video.")
            st.stop()

    if not os.path.exists(AUDIO_FILE):
        st.error("❌ Audio file not found. This video may be unsupported.")
        st.stop()

    with st.spinner("🧠 Transcribing with Whisper..."):
        transcript = transcribe_audio()

    st.success("Transcript generated successfully ✅")

    with st.spinner("✨ Creating AI summary..."):
        summary = summarize_text(transcript)

    st.subheader("📌 AI Summary")
    st.markdown(summary)

    with st.expander("📝 View Full Transcript"):
        st.text_area("Transcript", transcript, height=300)

    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)

