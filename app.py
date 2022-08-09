import io
from flask import Flask, request
from PIL import Image
import argparse
import json
from youtube_videos_capture_frames import capture, update, get_info
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/start', methods=["POST"])
def start():  # put application's code here
    if request.files.get("image"):
        # Method 1
        # with request.files["image"] as f:
        #     im = Image.open(io.BytesIO(f.read()))

        # Method 2
        im_file = request.files["image"]
        im_bytes = im_file.read()
        im = Image.open(io.BytesIO(im_bytes))
        print(im)
        im.save("img1.png")
        capture(
            "https://www.youtube.com/watch?v=Ej3N93Bdp-Q",
            [
                [[250, 340], [825, 1075]]
            ]
        )

@app.route('/update_photo', methods=["PUT"])
def update_photo():  # put application's code here
    if request.files.get("image"):
        # Method 1
        # with request.files["image"] as f:
        #     im = Image.open(io.BytesIO(f.read()))

        # Method 2
        im_file = request.files["image"]
        im_bytes = im_file.read()
        im = Image.open(io.BytesIO(im_bytes))
        # print(im)
        im.save("img1.png")
        update(
            [
                [[250, 340], [825, 1075]]
            ]
        )
        return "Done"

@app.route('/get_info', methods=["GET"])
def get_data():
    return json.dumps(get_info())


if __name__ == '__main__':
    app.run()
    # parser = argparse.ArgumentParser(description="Cars Counting Camera Live Zandvoort Boulevard")
    # parser.add_argument("--port", default=5002, type=int, help="port number")
    # opt = parser.parse_args()
    # app.run(host="0.0.0.0", port=5002)
