# this file controls the spotify api
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json

# load environment variables
load_dotenv()

# asks spotify if you can access the data
auth_manager = SpotifyClientCredentials(
    client_id = os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
)

# create the connection with Spotify
sp = spotipy.Spotify(auth_manager=auth_manager)

# function that returns the track ID of a specfic track
def getTrackID(song_name: str, artist_name: str) -> str | None:

    print("Inside the getTrackID function and the Spotify file")

    query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=query, type="track", limit=1)

    tracks = results.get("tracks", {}).get("items")
    return tracks[0]["id"] if tracks else None


def getTrackAnalysis(track_id: str) -> dict | None:

    print("Inside getTrackAnalysis in spotify file")
    print("Track ID from inside getTrackAnalysis: ",track_id)

    url = f"https://track-analysis.p.rapidapi.com/pktx/spotify/{track_id}"

    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
		'x-rapidapi-host': 'track-analysis.p.rapidapi.com'
    }
    
    response = requests.get(url, headers=headers)

    # For debugging purposes
    # print("STATUS CODE:", response.status_code)
    # print("RESPONSE TEXT:", response.text)

    return response.text

def getAudioFeatures(data) -> dict:
    # parse through the string
    if isinstance(data, str):
        data = json.loads(data)

    # should be a dict but just in case
    if not isinstance(data, dict):
        print("Invalid data format: ", type(data))
        return {}
    
    loudness_raw = data.get("loudness")
    loudness = int(loudness_raw.replace(" dB", "")) if loudness_raw else None

    return {
        "key": data.get("key"),
        "mode": data.get("mode"),
        "tempo": data.get("tempo"),
        "energy": data.get("energy"),
        "loudness": loudness
    }