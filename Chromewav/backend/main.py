# file that runs all of the backend code
from backend.personalization.personlization_state import personlizations
from backend.generation.prompt_builder import getPrompt
from backend.api.request_image import APIFrameClient
from backend.api.fetch_image import fetchImage
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()


print("\nrunning in main.py")
def main():

    # input data
    user_data = personlizations()

    if user_data is not None:
        # use the data to fill in the prompt  
        prompt = getPrompt(user_data)
        print("Prompt from the main file: ", prompt)
    
    if prompt is not None:
        #input the prompt into requesting the image and return the task id
        api_key = os.getenv("APIFRAME_KEY")
        client = APIFrameClient(api_key)
        task_id = client.requestImage(prompt, user_data.ratio)

        # use the task id to get the image link and download to computer 
        fetch = fetchImage(api_key)
        image_link = fetch.getImage(task_id, user_data.artist, user_data.song)
        print("Image link from main.py file: ", image_link)


if __name__ == "__main__":
    main()