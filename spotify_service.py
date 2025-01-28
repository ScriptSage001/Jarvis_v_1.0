import spotipy
from spotipy.oauth2 import SpotifyOAuth

from tts_engine_service import speak

# Define your app credentials
CLIENT_ID = "your_spotify_client_id"
CLIENT_SECRET = "your_spotify_client_secret"
REDIRECT_URI = "http://localhost:8888/callback"

# Initialize Spotify client
scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
                                            client_id = CLIENT_ID,
                                            client_secret = CLIENT_SECRET,
                                            redirect_uri = REDIRECT_URI,
                                            scope = scope))


def search_and_play_on_spotify(query):
    query = query.lower().replace("play", "").replace("on spotify", "").strip()

    """Search for a song/playlist/album and play it on Spotify."""
    try:
        # Search for the query
        results = sp.search(q = query, type = "track,playlist,album", limit = 1)

        if results["tracks"]["items"]:
            # Get the track URI
            track_uri = results["tracks"]["items"][0]["uri"]
            speak(f"Playing track {results['tracks']['items'][0]['name']} by {results['tracks']['items'][0]['artists'][0]['name']}")
        elif results["playlists"]["items"]:
            # Get the playlist URI
            track_uri = results["playlists"]["items"][0]["uri"]
            speak(f"Playing playlist {results['playlists']['items'][0]['name']}")
        elif results["albums"]["items"]:
            # Get the album URI
            track_uri = results["albums"]["items"][0]["uri"]
            speak(f"Playing album {results['albums']['items'][0]['name']}")
        else:
            speak("No results found on Spotify.")
            return

        # Play the track/playlist/album
        sp.start_playback(uris = [track_uri])
    except Exception as e:
        print(f"Error: {e}")

def spotify_controls(action):
    """Control playback (play, pause, next, previous)."""
    try:
        if action == "play":
            sp.start_playback()
            print("Resumed playback.")
        elif action == "pause":
            sp.pause_playback()
            print("Paused playback.")
        elif action == "next":
            sp.next_track()
            print("Skipped to next track.")
        elif action == "previous":
            sp.previous_track()
            print("Went to previous track.")
        else:
            print("Invalid action.")
    except Exception as e:
        print(f"Error: {e}")