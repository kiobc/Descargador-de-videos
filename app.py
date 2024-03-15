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
            output = path + '%(title)s.%(ext)s'
            # Ejecuta yt-dlp para descargar el video en formato mp4
            result = subprocess.run([
                "yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=webm]/best",
                "--ffmpeg-location", r"C:\webm\bin",
                "-o", output,
                url
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Imprime la salida y los errores de yt-dlp
            print(result.stdout.decode())
            print(result.stderr.decode())
            # Encuentra el archivo mp4 descargado
            for file in os.listdir(path):
                if file.endswith('.mp4'):
                    output_mp4 = os.path.join(path, file)
                    return send_file(output_mp4, as_attachment=True)
    except Exception as e:
        print(e)
        return f"Error: {str(e)}"
    return "Ocurrió un error durante la descarga del video."


@app.route('/envia2', methods=['POST'])
def envia2():
    try:
        if request.method == 'POST':
            url = request.form['url']
            output_webm = path + '%(title)s.%(ext)s'
            # Asegúrate de que yt-dlp use la ubicación correcta de ffmpeg
            subprocess.run([
                "yt-dlp",
                "-x",
                "--audio-format", "webm",
                "--ffmpeg-location", r"C:\webm\bin",
                "-o", output_webm,
                url
            ])
            # Encuentra el archivo webm descargado
            for file in os.listdir(path):
                if file.endswith('.webm'):
                    input_webm = os.path.join(path, file)
                    output_mp3 = os.path.splitext(input_webm)[0] + '.mp3'
                    # Convierte webm a mp3 utilizando la ubicación de ffmpeg
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