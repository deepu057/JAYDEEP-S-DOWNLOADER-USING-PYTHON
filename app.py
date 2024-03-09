from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('videoUrl')
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        download_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Jaydeep')
        os.makedirs(download_path, exist_ok=True)
        
        # Determine file extension based on whether audio-only download is requested
        file_extension = '.mp4'
        if 'audio' in request.form:
            stream = yt.streams.filter(only_audio=True).first()
            file_extension = '.mp3'

        video_filename = f'{yt.title}.{file_extension}'
        video_filepath = os.path.join(download_path, video_filename)

        # Download the video
        stream.download(download_path)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)
