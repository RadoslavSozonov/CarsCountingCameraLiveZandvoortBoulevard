import cv2


class Edge_detection:
    # # zandvoort/edge_detection/
    # def edge_detection(self, path, whee_to_put):
    #     name_of_photos = [
    #         'north_beach.jpg',
    #         'north_parking.jpg',
    #         'center.jpg',
    #         'center_south.jpg',
    #         'south.jpg'
    #     ]
    #     where_to_look = "zandvoort/edge_detection_name_of _photos/"
    #     for i in range(len(name_of_photos)):
    #         print(i+1)
    #         image = cv2.imread(path+name_of_photos[i])
    #         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #         edges = cv2.Canny(gray, threshold1=400, threshold2=500)
    #         # where_to_save = where_to_put + str(i+1)+'.jpg'
    #         cv2.imwrite(where_to_look+name_of_photos[i], edges)

    def edge_detection_detect(self, image1):
        # input = [['HISTCMP_CORREL.txt', cv2.HISTCMP_CORREL], ['HISTCMP_CHISQR.txt', cv2.HISTCMP_CHISQR],['HISTCMP_INTERSECT.txt', cv2.HISTCMP_INTERSECT]]

        # his = HistogramComparison()
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        edges1 = cv2.Canny(gray1, threshold1=100, threshold2=200)

        # gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        # edges2 = cv2.Canny(gray2, threshold1=100, threshold2=200)

        return edges1
        # result = his.compareOpenCV(edges1, edges2, cv2.HISTCMP_CORREL)
        # return result