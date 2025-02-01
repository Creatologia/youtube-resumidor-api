from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es', 'en'])
        return transcript
    except Exception as e:
        return f"Error: {e}"

def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=100, min_length=50, do_sample=False)
    
    return f"\n🔹 **Resumen del video:**\n\n📌 {summary[0]['summary_text']}\n"

# Cambia este ID por el de tu video
video_id = "dQw4w9WgXcQ"  

transcript = get_transcript(video_id)

if isinstance(transcript, list):
    text = " ".join([entry["text"] for entry in transcript[:300]])
    summary = summarize_text(text)
    print(f"\n📌 Resumen del video:\n{summary}")
else:
    print(transcript)

def generate_timestamps(transcript, video_id):
    timestamps = []
    for entry in transcript[:5]:  # Solo los primeros 5 timestamps para no sobrecargar
        time_in_seconds = int(entry["start"])
        minutes = time_in_seconds // 60
        seconds = time_in_seconds % 60
        url = f"https://www.youtube.com/watch?v={video_id}&t={time_in_seconds}s"
        timestamps.append(f"- [{minutes}:{seconds:02d}]({url}) {entry['text'][:50]}...")
    
    return "\n".join(timestamps)

timestamps_text = generate_timestamps(transcript, "dQw4w9WgXcQ")
print("\n🎯 **Timestamps Importantes:**\n", timestamps_text)