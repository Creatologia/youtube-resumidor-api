from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

def get_transcript(video_id):
    """Obtiene la transcripción de un video de YouTube."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es', 'en'])
        return transcript
    except Exception as e:
        return f"Error: {e}"

def summarize_text(text):
    """Resume el texto usando un modelo de IA."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=100, min_length=50, do_sample=False)
    return summary[0]["summary_text"]

@app.route('/resumir', methods=['GET'])
def resumir():
    """Recibe un ID de video y devuelve su resumen."""
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"error": "Falta el ID del video"}), 400

    transcript = get_transcript(video_id)
    if isinstance(transcript, str):  # Error en la transcripción
        return jsonify({"error": transcript})

    text = " ".join([entry["text"] for entry in transcript[:300]])
    summary = summarize_text(text)

    return jsonify({"video_id": video_id, "resumen": summary})

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Usa el puerto que Render asigna
    app.run(debug=True, host='0.0.0.0', port=port)