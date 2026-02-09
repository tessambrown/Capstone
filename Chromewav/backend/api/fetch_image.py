# This file takes in the task ID from request image and returns a link to the generated image

import requests
import time
import os
import json

class fetchImage:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.apiframe.pro"

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.api_key
            }
        
        # resolve to the project root Chromewav/
        # ".." means go up one directory level so first ".." -> /backend, second ".." -> /Chromewav
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        
        self.image_dir = os.path.join(self.project_root, "generated_images")
        os.makedirs(self.image_dir, exist_ok = True)
    
    def getFilePath(self, filename):
        name, ext = os.path.splitext(filename)
        path = os.path.join(self.image_dir, filename)

        counter = 1
        while os.path.exists(path):
            if counter == 1:
                new_name = f"{name}_copy{ext}"
            else:
                new_name = f"{name}_copy{counter}{ext}"

            path = os.path.join(self.image_dir, new_name)
            counter += 1

        return path

    # add a wait + poll + retrive result 
    def getImage(self, task_id, artist, song_name, max_retries = 20, wait_seconds = 3):
        url = f"{self.base_url}/fetch"
        
        for attempt in range(1, max_retries + 1):
            print(f"Fetch attempt: {attempt}/{max_retries}")

            response = requests.post(
                url,
                headers = self.headers,
                json = {"task_id": task_id}
            )

            data = response.json()
            status = data.get("status")
            print("Status: ", status)

            if status != "finished":
                time.sleep(wait_seconds)
                continue

            image_urls = data.get("image_urls", [])
            if not image_urls:
                print("Finished but no images")
                return None
            
            image_url = image_urls[0]

            # download the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            base_filename = f"{artist}_{song_name}.png"
            file_path = self.getFilePath(base_filename)


            # how python safely writes binary files 
            with open(file_path, "wb") as f:
                # png data 
                f.write(image_response.content)
            
            print("Image saved to: ", file_path)
            return file_path
        
        print("Times out waiting for image.")
        return None


