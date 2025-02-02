from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import os

app = Flask(__name__)  # Asegúrate de que la variable se llama "app"

@app.route('/')
def home():
    return jsonify({"status": "API funcionando correctamente"}), 200

@app.route('/transcripcion', methods=['GET'])
def transcripcion():
    """Devuelve la transcripción completa del video sin resumir."""
    video_id = request.args.get('video_id')

    if not video_id:
        return jsonify({"error": "Falta el ID del video"}), 400

    transcript = get_transcript(video_id)

    if "error" in transcript:
        return jsonify(transcript)

    return jsonify({"video_id": video_id, "transcripcion": transcript})

def get_transcript(video_id):
    """Obtiene la transcripción de un video de YouTube."""
    try:
        print(f"Intentando obtener la transcripción del video: {video_id}")  # 👀 Log de depuración
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es', 'en'])
        print("Transcripción obtenida correctamente")  # 👀 Confirma si la API responde
        return transcript
    except Exception as e:
        print(f"Error al obtener la transcripción: {e}")  # 🔹 Muestra el error exacto en los logs
        return {"error": str(e)}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)