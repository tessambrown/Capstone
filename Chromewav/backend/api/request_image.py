# This file takes in the prompt, calls the MJ API and request the image, returns the task ID
import requests

class APIFrameClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.apiframe.ai/pro"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

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


        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()

        data = response.json()
        task_id = data.get("task_id")

        if not task_id:
            raise ValueError("No task_id returned from API") 

        print("\ntask ID from request image file: ", task_id)
        return task_id

