from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def fetch_transcript(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try English first
        transcript = transcripts.find_transcript(['en'])

        data = transcript.fetch()
        full_text = " ".join([t["text"] for t in data])
        return full_text

    except TranscriptsDisabled:
        return "❌ Transcripts disabled for this video."

    except NoTranscriptFound:
        return "❌ No transcript found for this video."

    except Exception as e:
        return f"❌ Error fetching transcript: {e}"
