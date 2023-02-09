import os
from dotenv import load_dotenv
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

DISCORD_TOKEN=os.getenv('DISCORD_TOKEN')
SPOTIFY_CLIENT_ID=os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET=os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI=os.getenv('SPOTIFY_REDIRECT_URI')

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                 client_secret=SPOTIFY_CLIENT_SECRET,
                                                 redirect_uri=SPOTIFY_REDIRECT_URI,
                                                 scope=['user-library-read', 'user-read-playback-state', 'user-modify-playback-state']))

def get_link_type(link):
    youtube_pattern_1 = re.compile(r"^(https://youtu.be/)([a-zA-Z0-9_-]+)")
    youtube_pattern_2 = re.compile(r"^(https://youtube.com/playlist\?)([a-zA-Z0-9_-]+)")
    youtube_pattern_3 = re.compile(r"^(https://www.youtube.com/playlist\?)([a-zA-Z0-9_-]+)")
    youtube_pattern_4 = re.compile(r"^(https://www.youtube.com/)([a-zA-Z0-9_-]+)")
    spotify_pattern_1 = re.compile(r"^(https://open.spotify.com/track/)([a-zA-Z0-9]+)")
    spotify_pattern_2 = re.compile(r"^(https://open.spotify.com/playlist/)([a-zA-Z0-9]+)")
    other_link= re.compile(r'^https?://')

    if re.match(youtube_pattern_2, link) or re.match(youtube_pattern_3,link):
        return "YouTube-Playlist"
    elif re.match(youtube_pattern_1, link) or re.match(youtube_pattern_4, link) :
        return "YouTube"
    elif re.match(spotify_pattern_1, link):
        return "Spotify-Track"
    elif re.match(spotify_pattern_2, link):
        return "Spotify-Playlist"
    elif re.match(other_link, link):
        return "Unknown"
    else:
        return "Song Name"
