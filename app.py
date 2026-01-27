from flask import Flask, render_template, jsonify, request, redirect
from ytmusicapi import YTMusic
import yt_dlp

app = Flask(__name__)
yt = YTMusic()

@app.route('/stream/<video_id>')
def stream_audio(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return redirect(info['url'])
    except Exception as e:
        print(f"Error streaming {video_id}: {e}")
        return jsonify({"error": "Failed to stream"}), 500

def search_tracks(query):
    try:
        # Search YouTube Music
        print(f"Searching YTMusic: {query}")
        results = yt.search(query, filter='songs', limit=20)
        
        tracks = []
        for item in results:
            if item['resultType'] == 'song':
                # Get extract artwork
                thumbnails = item.get('thumbnails', [])
                cover = thumbnails[-1]['url'] if thumbnails else 'https://via.placeholder.com/300'
                
                tracks.append({
                    "id": item['videoId'],
                    "title": item['title'],
                    "artist": item['artists'][0]['name'] if item.get('artists') else 'Unknown',
                    "duration": item.get('duration', '0:00'),
                    "cover": cover,
                    "cover_xl": cover.replace('w60-h60', 'w500-h500') # Access high res
                })
        print(f"Found {len(tracks)} tracks")
        return tracks
    except Exception as e:
        print(f"Error fetching tracks: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def search():
    query = request.args.get('q', 'Hindi Top 50') # Default search if empty
    results = search_tracks(query)
    return jsonify(results)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "vibestream-player"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
