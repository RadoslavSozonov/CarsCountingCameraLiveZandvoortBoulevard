import cv2
from vidgear.gears import CamGear
from edge_detection import Edge_detection
import requests
import datetime
photo_to_compare = []
detected_photos_info = []
# DETECTION_URL = "http://localhost:5010/get_count"
DETECTION_URL = "http://localhost:5002/cars-counting"
IMAGE = "image.jpg"

def get_info():
    print(detected_photos_info)
    return detected_photos_info

def update(photos_detail):
    edge_detection = Edge_detection()
    photo_to_compare = []
    for zone in photos_detail:
        frame = cv2.imread("img1.png")
        y_zone = zone[0]
        x_zone = zone[1]
        cropped_image = frame[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
        cropped_image = edge_detection.edge_detection_detect(cropped_image)
        photo_to_compare = []
        photo_to_compare.append(cropped_image)

def capture(url_video, photos_detail):
    edge_detection = Edge_detection()
    photo_to_compare = []
    detected_photos_info = []
    for zone in photos_detail:
        frame = cv2.imread("img1.png")
        y_zone = zone[0]
        x_zone = zone[1]
        cropped_image = frame[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
        cropped_image = edge_detection.edge_detection_detect(cropped_image)
        photo_to_compare.append(cropped_image)
    # the video stream
    # prev_res = []
    # for i in range(len(photos_details)):
    #     prev_res.append(0)
    prev_res = []
    prev_res.append(0)

    loop = 1
    counter = 1
    # file = open("MyFile.txt", "a")
    count = 1
    stream = CamGear(source=url_video, stream_mode=True, time_delay=5,
                     logging=True).start()
    while True:

        skip = 0
        if count % 10000 == 0:
            stream = CamGear(source=url_video, stream_mode=True, time_delay=5,
                             logging=True).start()

        for i in range(loop):
            frame = stream.read()  # using functions from vidGear module
            # print(type(frame))
            if str(type(frame)) != "<class 'numpy.ndarray'>":
                stream = CamGear(source=url_video, stream_mode=True, time_delay=5,
                                 logging=True).start()
                continue
        loop = 30
        # if count < 10000:
        #     print(count)
        # cv2.imwrite('zandvoort/extracted_images/' + str(count) + '.jpg', frame)
        # to_write = str(count) + ". "
        # print(count)
        metric_val_average = []
        for zone in photos_detail:
            y_zone = zone[0]
            x_zone = zone[1]
            cropped_image = frame[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
            cropped_image = edge_detection.edge_detection_detect(cropped_image)
            result = compare_edges_only(photo_to_compare[0], cropped_image)

            metric_val_average.append(result)
        result = round(sum(metric_val_average) / len(metric_val_average), 4)
        skip = write_to_directory(result, counter, photo_to_compare, cropped_image, prev_res, frame)
        # to_write += str(round(result, 3)) + " "
        if skip > 0:
            break
        count += 1

        # to_write += '\n'
        # file.write(to_write)

    cv2.destroyAllWindows()
    stream.stop()
    stream.stop()

def write_to_directory(result, counter, photo_to_compare, cropped_image, prev_res, frame):
    threshold = 0.21
    print(result)
    if result >= threshold:
        if result > prev_res[0]:
            if prev_res[0] < threshold:
                counter += 1
                # print("Match")
            cv2.imwrite(IMAGE, frame)
            with open(IMAGE, "rb") as f:
                image_data = f.read()
            # print(image_data)
            response = requests.post(DETECTION_URL, files={"image": image_data}).json()
            # print(response)
            detected_photos_info.append({
                "people": str(response),
                "counter": counter,
                "time": str(datetime.datetime.now())
            })
            prev_res[0] = result
            photo_to_compare[0] = cropped_image
        return 0
    prev_res[0] = 0
    return 0

def compare_edges_only(image1, image2):
    white_cells_image1 = 0
    white_cells_image2 = 0
    counter1 = 0
    counter2 = 0
    for i in range(len(image1)):
        for y in range(len(image1[0])):
            if image1[i][y] != 0:
                white_cells_image1 += 1
            if image2[i][y] != 0:
                white_cells_image2 += 1
            if image1[i][y] != 0 and image2[i][y] != 0:
                counter2 += 1
    counter1 = max(1, counter1)
    counter2 = max(1, counter2)
    try:
        pers1 = round(counter1 / white_cells_image1, 4)
    except:
        pers1 = 0
    try:
        pers2 = round(counter2 / white_cells_image2, 4)
    except:
        pers2 = 0
    return (pers2) / 2