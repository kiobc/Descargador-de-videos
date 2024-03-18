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
            result = subprocess.run([
                "yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=webm]/best",
                "--ffmpeg-location", r"C:\webm\bin",
                "-o", output,
                url
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode())
            print(result.stderr.decode())
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
    if request.method == 'POST':
        url = request.form['url']
        output_webm = path + '%(title)s.%(ext)s'
        try:
            subprocess.run([
                "yt-dlp",
                "-x",
                "--audio-format", "mp3", 
                "--ffmpeg-location", r"C:\webm\bin",
                "-o", output_webm,
                url
            ], check=True)
            for file in os.listdir(path):
                if file.endswith('.mp3'):
                    output_mp3 = os.path.join(path, file)
                    return send_file(output_mp3, as_attachment=True)
        except subprocess.CalledProcessError as e:
            print(e)
            return "Error al descargar o convertir el archivo."
        except Exception as e:
            print(e)
            return "Ocurrió un error inesperado."
    return "No se pudo procesar la solicitud."



if __name__ == '__main__':
    app.run(host='localhost')