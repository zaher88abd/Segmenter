import cv2
import imutils
from PyQt5.QtGui import *


def covertGrayRGB(gray):
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def get_image_format(image):
    qformat = QImage.Format_Indexed8
    if len(image.shape) == 3:
        if (image.shape[2]) == 4:
            qformat = QImage.Format_RGBA8888
        else:
            qformat = QImage.Format_RGB888

    return qformat


def Zoom(cv2Object, zoomSize):
    # try:
    # Resizes the image/video frame to the specified amount of "zoomSize".
    # A zoomSize of "2", for example, will double the canvas size
    cv2Object = imutils.resize(cv2Object, width=(zoomSize * cv2Object.shape[1]))
    # center is simply half of the height & width (y/2,x/2)
    center = (cv2Object.shape[0] / 2, cv2Object.shape[1] / 2)
    # cropScale represents the top left corner of the cropped frame (y/x)
    cropScale = (center[0] / zoomSize, center[1] / zoomSize)
    # The image/video frame is cropped to the center with a size of the original picture
    # image[y1:y2,x1:x2] is used to iterate and grab a portion of an image
    # (y1,x1) is the top left corner and (y2,x1) is the bottom right corner of new cropped frame.
    cv2Object = cv2Object[int(cropScale[0]):int(center[0] + cropScale[0]),
                int(cropScale[1]):int(center[1] + cropScale[1])]
    return cv2Object
    # except Exception as e:
    #     print(e)


def crop(img, x, y):
    x_0 = x - 90
    x_1 = x + 90

    y_0 = y - 70
    y_1 = y + 70
    crop_img = img[y_0:y_1, x_0:x_1]
    return crop_img
