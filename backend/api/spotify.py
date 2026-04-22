# this file controls the spotify api
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json

# For local deployment
from backend.errors import appError

# For Render deployment
# from errors import appError

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

    # set the song name and the artist name in a string
    query = f"track:{song_name} artist:{artist_name}"

    # use the query string to search and return a result
    results = sp.search(q=query, type="track", limit=1)

    tracks = results.get("tracks", {}).get("items")

    if tracks is None:
        raise appError("Failed to find song id", 404)

    # return the id of the track
    return tracks[0]["id"]

# input the track id and return metadata
def getTrackAnalysis(track_id: str) -> dict | None:

    # add the track ID to the search url
    url = f"https://track-analysis.p.rapidapi.com/pktx/spotify/{track_id}"

    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
		'x-rapidapi-host': 'track-analysis.p.rapidapi.com'
    }
    
    # use the url to search for the meta data and add headers to the 
    response = requests.get(url, headers=headers)
    print("Track analysis response (fix error accordingly)", response)

    # if response != 200:
    #     raise appError("Failed to get song metadata", 404)

    return response.text

def getAudioFeatures(data) -> dict:
    # parse through the string
    if isinstance(data, str):
        data = json.loads(data)

    # should be a dict but just in case
    if not isinstance(data, dict):
        raise appError("Invalid data format", 500)
    
    # seperate the loudness from the data and remove dB
    loudness_raw = data.get("loudness")
    loudness = int(loudness_raw.replace(" dB", "")) if loudness_raw else None

    # validateAudioFeatures(data.get("key"), data.get("mode"), data.get("tempo"), data.get("energy"), loudness, data.get("happiness"))

    return {
        "key": data.get("key"),
        "mode": data.get("mode"),
        "tempo": data.get("tempo"),
        "energy": data.get("energy"),
        "loudness": loudness,
        "happiness": data.get("happiness")
    }


def validateAudioFeatures(key, mode, tempo, energy, loudness, happiness):

    # validate key
    if not isinstance(key, str) or not key.strip():
        raise appError("Cannot find song key", 500)
    
    # validate mode
    if not isinstance(mode, str) or not mode.strip():
        raise appError("Cannot find song mode", 500)
    
    # validate tempo
    if not isinstance(tempo, str) or not tempo.strip():
        raise appError("Cannot find song tempo", 500)
    
    # validate energy
    if not isinstance(energy, str) or not energy.strip():
        raise appError("Cannot find song energy", 500)
    
    # validate loudness
    if not isinstance(loudness, int):
        raise appError("Cannot find song loudness", 500)
    
    # validate happiness
    if not isinstance(happiness, str) or not happiness.strip():
        raise appError("Cannot find song happiness", 500)