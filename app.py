from flask import Flask, render_template, request, send_file
import os
import subprocess  

app = Flask(__name__)
path = os.getcwd() + '/output/'

if not os.path.exists(path):
    os.makedirs(path)

@app.route('/')
def route():
    return render_template('index.html')

@app.route('/envia', methods=['POST'])
def envia():
    try:
        if request.method == 'POST':
            url = request.form['url']
            output = path + 'video.mp4'
            subprocess.run(["yt-dlp", "-o", output, url])
            return send_file(output, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/envia2', methods=['POST'])
def envia2():
    try:
        if request.method == 'POST':
            url = request.form['url']
            output_webm = path + '%(title)s.%(ext)s'
            subprocess.run([
                "yt-dlp",
                "-x",
                "--audio-format", "webm",
                "--ffmpeg-location", r"C:\webm\bin",
                "-o", output_webm,
                url
            ])
            for file in os.listdir(path):
                if file.endswith('.webm'):
                    input_webm = os.path.join(path, file)
                    output_mp3 = os.path.splitext(input_webm)[0] + '.mp3'
                    subprocess.run([
                        r"C:\webm\bin\ffmpeg",
                        "-i", input_webm,
                        "-vn",
                        "-ab", "128k",
                        "-ar", "44100",
                        "-y", output_mp3
                    ])
                    return send_file(output_mp3, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"
    return "Ocurrió un error durante la descarga o la conversión del archivo."

if __name__ == '__main__':
    app.run(host='localhost')