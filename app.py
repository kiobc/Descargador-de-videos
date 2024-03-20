from flask import Flask, render_template, request, send_file
import os
import subprocess  
import json
import requests

app = Flask(__name__)
path = os.getcwd() + '/output/'

if not os.path.exists(path):
    os.makedirs(path)

def download_thumbnail(url, output_path):
    try:
        subprocess.run([
            "yt-dlp",
            "--skip-download",  
            "--write-thumbnail", 
            "--output", output_path,
            url
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False

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

def download_video(url, output_path):
    try:
        subprocess.run([
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "-o", output_path,
            url
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False

def extract_thumbnail(video_path, thumbnail_path):
    try:
        subprocess.run([
            "ffmpeg",
            "-i", video_path,
            "-ss", "00:00:01", 
            "-vframes", "1",  
            thumbnail_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False

@app.route('/envia2', methods=['POST'])
def envia2():
    if request.method == 'POST':
        url = request.form['url']
        result = subprocess.run(["yt-dlp", "-j", "--skip-download", url], stdout=subprocess.PIPE, text=True)
        video_info = json.loads(result.stdout)
        
        thumbnail_url = video_info.get("thumbnail")
        title = video_info.get("title").replace('"', '')  
        video_path = os.path.join(path, f"{title}.mp4")
        thumbnail_path = os.path.join(path, f"{title}_thumbnail.jpg")
        output_mp3 = os.path.join(path, f"{title}.mp3")
        
        try:
            subprocess.run(["yt-dlp", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", "-o", video_path, url], check=True)
            
            response = requests.get(thumbnail_url)
            with open(thumbnail_path, 'wb') as file:
                file.write(response.content)
            
            subprocess.run([
                "ffmpeg",
                "-i", video_path,
                "-i", thumbnail_path,
                "-map", "0:a", 
                "-map", "1:v",  
                "-codec:v", "copy",  
                "-codec:a", "libmp3lame",  
                "-q:a", "0", 
                "-id3v2_version", "3",  
                "-metadata:s:v", "title=\"Album cover\"",  
                "-metadata:s:v", "comment=\"Cover (front)\"", 
                output_mp3
            ], check=True)
            
            return send_file(output_mp3, as_attachment=True)
        except subprocess.CalledProcessError as e:
            print(e)
            return "Error al descargar, convertir o extraer miniatura del archivo."
        except Exception as e:
            print(e)
            return "Ocurrió un error inesperado."
    return "No se pudo procesar la solicitud."


if __name__ == '__main__':
    app.run(host='localhost')