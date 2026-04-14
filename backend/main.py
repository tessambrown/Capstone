# For local deployment
# from backend.song_data.song_data import songMetadata
# from backend.build.prompt_builder import getPrompt
# from backend.api.request_image import APIFrameClient
# from backend.api.fetch_image import fetchImage
# from backend.song_data.helper_functions import validateInputs
# from backend.errors import appError, registerErrorHandlers

# For Render deployment
from song_data.song_data import songMetadata
from build.prompt_builder import getPrompt
from api.request_image import APIFrameClient
from api.fetch_image import fetchImage
from song_data.helper_functions import validateInputs
from errors import appError, registerErrorHandlers

# import other helpful elements
from dotenv import load_dotenv
import os

# load environment variables for API keys
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
registerErrorHandlers(app)

CORS(app, origins=["http://chromewav.com", "https://tessambrown.github.io"])
# CORS(app, origins=["http://[::]:5050"])

@app.route("/personlization", methods=["POST"])
def personlization():

    print("Request recived!")

    data = request.json
    print("Data:", data)

    # get the data and validate input
    artist_input, song_input, canvas_input = validateInputs(
        data.get("artistInput"),
        data.get("songInput"),
        data.get("canvasInput")
    ) 

    # input user input and get song data
    user_data = songMetadata(artist_input, song_input, canvas_input)

    # check if songMetadata needs confirmation
    if isinstance(user_data, dict) and user_data.get("needs_confirmation"):
        return jsonify(user_data), 202

    prompt = getPrompt(user_data)
    if prompt is None:
        raise appError("Failed to generate prompt", 500)

    api_key = os.getenv("APIFRAME_KEY")
    if not api_key:
        raise appError("Missing API key", 500)

    client = APIFrameClient(api_key)

    # generate image and return the task id for the image
    task_id = client.requestImage(prompt, user_data.ratio)
    if task_id is None:
        raise appError("Failed to generate image", 500)
    
    # send the api key and get fetch 
    fetch = fetchImage(api_key)
    image_link = fetch.getImage(task_id)
    if image_link is None:
        raise appError("Failed to get image link", 500)
    
    print("image link:", image_link)
    
    # return the image url + lyrics
    return jsonify({
        "imageUrl": image_link,
        "lyrics": user_data.lyrics,
        "artist": user_data.artist,
        "song": user_data.song,
        "ratio": user_data.ratio
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# for just the backend (use for testing)
# def main():

#     artist = "ROSALIA"
#     song = "Berghain"
#     canvas_type = "poster"

#     # validate input 
#     artist, song, canvas_type = validateInputs(artist, song, canvas_type)

#     # input user input and get song data
#     user_data = songMetadata(artist, song, canvas_type)

#     # check if songMetadata needs confirmation
#     if isinstance(user_data, dict) and user_data.get("needs_confirmation"):
#         return jsonify(user_data), 202

#     # use song data to create a prompt
#     prompt = getPrompt(user_data)
#     if prompt is None:
#         raise appError("Failed to generate prompt", 500)

#     api_key = os.getenv("APIFRAME_KEY")
#     if not api_key:
#         raise appError("Missing API key", 500)

#     client = APIFrameClient(api_key)

#     # generate image and return the task id for the image
#     task_id = client.requestImage(prompt, user_data.ratio)
#     if task_id is None:
#         raise appError("Failed to generate image", 500)

#     print("Task ID:", task_id)

#     # send the api key and get fetch 
#     fetch = fetchImage(api_key)
#     image_link = fetch.getImage(task_id)
#     if image_link is None:
#         raise appError("Failed to get image link", 500)    
    
#     print("Image link:", image_link)


# if __name__ == "__main__":
#     # run main() for just the backend
#     main()