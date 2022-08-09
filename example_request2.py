import pprint

import requests

DETECTION_URL = "http://localhost:5000/get_info"
IMAGE = "2.jpg"

# Read image
with open(IMAGE, "rb") as f:
    image_data = f.read()

response = requests.get(DETECTION_URL)

pprint.pprint(response.text)
