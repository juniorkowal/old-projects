import cv2
import os
import numpy as np
temp2 = []
temp3 = []
hero = []
i = 0
j = 0
number_of_pictures = 1
width = 45 * number_of_pictures
height = 85
path_to_directory = "C:/Users/admin/PycharmProjects/jednostki/ds/2dwojki"
for dirname in os.listdir(path_to_directory):
    temp2.append(dirname)
    temp3.append(i)
    i = i + 1
    for filename in os.listdir(os.path.join(path_to_directory, dirname)):
        img = cv2.imread(os.path.join(path_to_directory, dirname, filename))

        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                if (img[x][y][0] == 255 and img[x][y][1] == 255 and img[x][y][2] == 0):
                    img[x][y] = [0, 0, 0]

        img_thresh = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img_thresh = cv2.threshold(img_thresh, 0, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(img_thresh, 1, 2)
        x, y, w, h = cv2.boundingRect(contours[len(contours)-2])
        #cv2.rectangle(img, (x, y), (x + w, y + h), (123, 78, 243), 2)
        w1 = w
        h1 = h
        if w > (45 * number_of_pictures):
            w1 = 45
        if h > 85:
            h1 = 85
        buff = np.zeros((height, width, 3), dtype='uint8')
        buff2 = np.zeros((height, width, 3), dtype='uint8')
        buff[(height - h1):height, 0:w1] = img[(y + (h - h1)):((y + h1) + (h - h1)), x:(x + w1)]
        buff2[(height - h1):height, 0:w1] = img[(y + (h - h1)):((y + h1) + (h - h1)), x + w1:(x + 2*w1)]
        img2 = cv2.flip(buff, 1)
        img3 = cv2.flip(buff2, 1)
        #cv2.imshow('asdas', buff)
        #cv2.waitKey(0)

        cv2.imwrite(dirname+str(j)+'.bmp', buff)
        cv2.imwrite(dirname + str(j) + '_mirror.bmp', img2)
        cv2.imwrite(dirname + str(j)+ '-2' + '.bmp', buff2)
        cv2.imwrite(dirname + str(j) + '-2' + '_mirror.bmp', img3)
        j += 1
