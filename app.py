from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    song_name = data.get('song_name', '')

    if not song_name:
        return jsonify({"error": "Название трека не указано"}), 400

    # Скачиваем MP3 через SpotDL
    subprocess.run(["spotdl", song_name])

    # Загружаем в Google Drive (rclone должен быть настроен)
    os.system(f"rclone copy '{song_name}.mp3' gdrive:/Music/")

    return jsonify({"status": "Downloaded", "file": f"{song_name}.mp3"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
