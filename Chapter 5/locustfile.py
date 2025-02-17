import os
import random
from io import BytesIO  
from locust import task, HttpUser

class MyUser(HttpUser):

    def get_image(self):
        rand_img = random.randint(0, 999)  
        filepath = os.path.join('./img', f'{rand_img:05}.png')

        try:
            with open(filepath, 'rb') as f:
                image_data = f.read()
                image_file = BytesIO(image_data)
                filename = os.path.basename(filepath)
                return rand_img, filename, image_file, 'image/png'

        except FileNotFoundError:
            print(f'Error: Image file not found: {filepath}')
            return None, None, None, None

    @task
    def index(self):
        rand_img, filename, image_file, content_type = self.get_image()

        if image_file: 
            files = {'image': (filename, image_file, content_type)}
            self.client.post(f'/classify?id={rand_img}', files=files)
        else:
            print('Skipping request due to missing image.')
