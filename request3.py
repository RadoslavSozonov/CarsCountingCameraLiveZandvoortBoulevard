import pprint

import requests

DETECTION_URL = "http://localhost:5000/update_photo"
IMAGE = "3.jpg"

# Read image
with open(IMAGE, "rb") as f:
    image_data = f.read()
response = requests.put(DETECTION_URL, files={"image": image_data})

pprint.pprint(response.text)