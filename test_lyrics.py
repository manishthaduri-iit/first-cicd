
from ytmusicapi import YTMusic
yt = YTMusic()

def test_lyrics(video_id):
    print(f"Testing lyrics for {video_id}...")
    try:
        watch_playlist = yt.get_watch_playlist(videoId=video_id)
        lyrics_id = watch_playlist.get('lyrics')
        print(f"Lyrics ID: {lyrics_id}")
        
        if lyrics_id:
            lyrics_data = yt.get_lyrics(lyrics_id)
            print("Lyrics found!")
            print(lyrics_data['lyrics'][:100] + "...")
        else:
            print("No lyrics ID found in watch playlist.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test with the song used in previous tests (The Weeknd - Blinding Lights)
    test_lyrics("4NRXx6U8ABQ") 
