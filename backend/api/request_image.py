# This file takes in the prompt, calls the MJ API and request the image, returns the task ID
import requests

# For local deployment
# from backend.errors import appError

# For Render deployment
from errors import appError

class APIFrameClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.apiframe.ai/pro"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }
    # add the prompt + aspect ratio and return the generated images task id
    def requestImage(self, prompt, ratio):
        print("\nrunning in request image file inside of requestImage\n")

        url = f"{self.base_url}/imagine"

        payload = {
            "prompt": prompt,
            "aspect_ratio": ratio,
        }

        print("DEBUG payload:", payload)
        print("DEBUG aspect_ratio:", ratio, type(ratio))
        print("DEBUG prompt type:", type(prompt))

        # requests.post() -> uses the request library to send a POST request
        # url -> API endpoint
        # json=payload -> sends a JSON body
        response = requests.post(url, json=payload, headers=self.headers)

        # check for the status of the response
        response.raise_for_status()
        # translate from json to python dict
        data = response.json()
        # seperate the task id 
        task_id = data.get("task_id")

        if not task_id:
            raise appError("Failed to get task ID", 500)
        # return task ID
        print("\ntask ID from request image file: ", task_id)
        return task_id
