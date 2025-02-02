from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from transformers import pipeline
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "API funcionando correctamente. Usa /resumir?video_id=<ID> para obtener resúmenes."})

@app.route('/resumir', methods=['GET'])
def resumir():
    """Obtiene y resume la transcripción de un video de YouTube."""
    video_id = request.args.get('video_id')

    if not video_id:
        return jsonify({"error": "Falta el parámetro 'video_id'"}), 400

    try:
        # Intentar obtener la transcripción del video
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es', 'en'])
        text = " ".join([entry["text"] for entry in transcript[:300]])

        # Si la transcripción está vacía, devolver un mensaje claro
        if not text:
            return jsonify({"error": "El video no tiene suficiente texto en la transcripción."}), 400

        # Usar IA para resumir el texto
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(text, max_length=100, min_length=50, do_sample=False)

        return jsonify({"video_id": video_id, "resumen": summary[0]["summary_text"]})

    except TranscriptsDisabled:
        return jsonify({"error": "Los subtítulos están deshabilitados para este video. Prueba con otro."}), 400

    except NoTranscriptFound:
        return jsonify({"error": "No se encontró ninguna transcripción en los idiomas disponibles. Prueba con otro video."}), 400

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {str(e)}"}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Usa el puerto asignado por Render
    app.run(host='0.0.0.0', port=port)