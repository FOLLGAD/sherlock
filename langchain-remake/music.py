import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search(artist = None, album = None, song = None, playlist = None):
    query = [a for a in [song, artist, album, playlist] if a is not None]
    query = "\n".join(query)
    search_type = "track" if song is not None else "playlist" if playlist is not None else "album" if album is not None else "artist"
    results = sp.search(q=query, type=search_type, limit=1)
    print(results)
    return results[search_type+"s"]["items"][0]

