import cv2
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
