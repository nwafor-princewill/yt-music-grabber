import os
import shutil
import atexit
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp

# ========== CONFIGURATION ==========
FFMPEG_DIR = r"C:\ffmpeg-2026-03-22-git-9c63742425-full_build\ffmpeg-2026-03-22-git-9c63742425-full_build\bin"
# ===================================

os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/get/<path:filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

atexit.register(lambda: shutil.rmtree(DOWNLOAD_FOLDER, ignore_errors=True))

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    format_type = data.get('format', 'mp3')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    if not (url.startswith('http') and ('youtube.com' in url or 'youtu.be' in url or 'soundcloud.com' in url)):
        return jsonify({'error': 'Invalid URL'}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': FFMPEG_DIR,
        'socket_timeout': 30,
    }

    if format_type == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'EmbedThumbnail',   # Embeds thumbnail into the MP3
                }
            ],
            'writethumbnail': True,            # Downloads the thumbnail
            'addmetadata': True,               # Adds metadata from the video
            'parse_metadata': [                # Optional: set artist from uploader
                'artist:%(uploader)s',
                'title:%(title)s',
            ],
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        })
    elif format_type == 'mp4':
        ydl_opts.update({
            'format': 'best[ext=mp4]',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        })
    else:  # webm
        ydl_opts.update({
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if format_type == 'mp3':
                base, _ = os.path.splitext(filename)
                filename = base + '.mp3'

            if not os.path.exists(filename):
                return jsonify({'error': 'File not created'}), 500

            return jsonify({
                'success': True,
                'file_url': f'/get/{os.path.basename(filename)}'
            })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    app.run(debug=True, port=5000)