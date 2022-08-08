import cv2
from vidgear.gears import CamGear
from scipy.ndimage.filters import gaussian_filter
from edge_detection import Edge_detection

class FrameCapture:
    def capture(self, url_video, photos_details, name_of_photos, to_store):
        edge_detection = Edge_detection()
        photos_to_compare = []
        for photo_details in photos_details:
            frame = cv2.imread(photo_details[0])
            for zone in photo_details[1]:
                y_zone = zone[0]
                x_zone = zone[1]
                cropped_image = frame[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
                cropped_image = edge_detection.edge_detection_detect(cropped_image)
                blurred = gaussian_filter(cropped_image, sigma=1)
                photos_to_compare.append(blurred)
        # the video stream
        prev_res = []
        for i in range(len(photos_details)):
            prev_res.append(0)

        loop = 1
        counter = {}
        for name in name_of_photos:
            counter[name] = 0
        file = open("MyFile.txt", "a")
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
            cv2.imwrite('zandvoort/extracted_images/' + str(count) + '.jpg', frame)
            to_write = str(count) + ". "
            print(count)
            for y in range(len(photos_details)):
                metric_val_average = []
                for zone in photos_details[y][1]:
                    y_zone = zone[0]
                    x_zone = zone[1]
                    cropped_image = frame[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
                    cropped_image = edge_detection.edge_detection_detect(cropped_image)
                    result = self.compare_edges_only(photos_to_compare[y], cropped_image)
                    metric_val_average.append(result)
                result = round(sum(metric_val_average) / len(metric_val_average), 4)
                skip = self.write_to_directory(result, frame, to_store[y], photos_details[y], counter, y,
                                               name_of_photos, photos_to_compare, cropped_image, prev_res)
                to_write += str(round(result, 3)) + " "
                if skip > 0:
                    break
            count += 1

            to_write += '\n'
            file.write(to_write)

        cv2.destroyAllWindows()
        stream.stop()
        stream.stop()

    def write_to_directory(self, result, frame, to_store, photo_details, counter, y, name_of_photos, photos_to_compare,
                           cropped_image, prev_res):
        threshold = 0.4
        if result >= threshold:
            if result > prev_res[y]:
                if prev_res[y] < threshold:
                    counter[name_of_photos[y]] += 1
                prev_res[y] = result
                cv2.imwrite(to_store + str(counter[name_of_photos[y]]) + '.jpg', frame)
                blurred = gaussian_filter(cropped_image, sigma=1)
                photos_to_compare[y] = blurred
                # skip = photo_details[2]
                print('found ' + str(y + 1), result)
            return 0
        prev_res[y] = 0
        return 0

    def compare_edges_only(self, image1, image2):
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