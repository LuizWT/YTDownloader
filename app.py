import subprocess
from flask import Flask, render_template, request, Response

app = Flask(__name__)

def stream_download(command, mimetype, filename):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    def generate():
        while True:
            chunk = process.stdout.read(4096)
            if not chunk:
                break
            yield chunk

    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return Response(generate(), mimetype=mimetype, headers=headers)

def download_video_to_memory(url):
    command = [
        'yt-dlp',
        '-f', 'mp4',
        '-o', '-',  # direciona a saída para stdout
        url
    ]

    return stream_download(command, mimetype="video/mp4", filename="LuizWT_YT_video_Downloader_.mp4")

def download_audio_to_memory(url):
    command = [
        'yt-dlp',
        '-x',
        '--audio-format', 'mp3',
        '--audio-quality', '192K',
        '-o', '-',  # direciona a saída para stdout
        url
    ]
    return stream_download(command, mimetype="audio/mpeg", filename="LuizWT_YT_audio_Downloader_.mp3")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        download_type = request.form['download_type']
        if download_type == 'video':
            return download_video_to_memory(url)
        elif download_type == 'audio':
            return download_audio_to_memory(url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
