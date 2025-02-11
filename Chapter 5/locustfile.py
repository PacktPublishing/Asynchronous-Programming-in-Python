import os
import random
from io import BytesIO  # For creating in-memory file-like objects
from locust import task, HttpUser

class MyUser(HttpUser):

    def get_image(self):
        rand_img = random.choice([1,4,7,10,16,19,21,25,35,52])
        filepath = os.path.join('./img', f'{rand_img}.png')  # More robust path handling

        try:
            with open(filepath, 'rb') as f: # Open in binary mode
                image_data = f.read()
                image_file = BytesIO(image_data) # Create a file-like object
                filename = os.path.basename(filepath)
                return rand_img, filename, image_file, 'image/png' # or appropriate content type

        except FileNotFoundError:
            print(f'Error: Image file not found: {filepath}')
            return None, None, None  # Handle the error

    @task
    def index(self):
        rand_img, filename, image_file, content_type = self.get_image()

        if image_file: # Check file exists
            files = {'image': (filename, image_file, content_type)}
            self.client.post(f'/classify?id={rand_img}', files=files)
        else:
            print('Skipping request due to missing image.')

