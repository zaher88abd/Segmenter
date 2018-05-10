from tkinter import filedialog
from tkinter import *
import numpy as np
import cv2
from pathlib import Path
import os

# set global parameters
WHITE = np.array([255, 255, 255])
BLACK = np.array([0, 0, 0])
RED = np.array([255, 0, 0])
GREEN = np.array([0, 255, 0])


def get_filters(filename):
    frame = cv2.imread(str(filename), flags=cv2.IMREAD_COLOR)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_black = np.array([50, 50, 50], dtype="uint16")
    upper_black = np.array([100, 255, 100], dtype="uint16")
    black_mask = cv2.inRange(hsv, lower_black, upper_black)

    lower_white = np.array([100, 100, 100], dtype="uint16")
    upper_white = np.array([255, 255, 255], dtype="uint16")
    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    return frame, black_mask, white_mask


def change_color(mask1, color1, mask2, colo2):
    img = np.zeros((mask1.shape[0], mask1.shape[1], 3))
    img[np.where(mask1 == 255)] = color1
    # img[np.where(mask2 == 255)] = colo2
    return img


root = Tk()
root.filename = filedialog.askopenfilename(initialdir="/home/zaher", title="Select file",
                                           filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

frame, black_mask, white_mask = get_filters(root.filename)
cv2.imshow("orogila", frame)
cv2.imshow("filter", change_color(mask1=black_mask, color1=RED, mask2=white_mask, colo2=GREEN))
cv2.waitKey(0)
# path_img = "C:\\Users\\zaher\\Pictures\\JPEG_Images"
# path_ann="C:\\Users\\zaher\\Pictures\\JPEG_Images"
# for dir_ in path_.iterdir():
#     if dir_.is_dir():
#         sub_path = Path(path_, dir_)
#         sub_save_path = str(dir_) + "seg"
#         if not os.path.exists(os.path.join(path_, sub_save_path)):
#             os.makedirs(os.path.join(path_, sub_save_path))
#         for img_name in sub_path.iterdir():
#             if not img_name.is_dir():
#                 img, black_mask, white_mask = get_filters(img_name)
#                 img = change_color(black_mask, np.array([0, 0, 255]), white_mask, np.array([255, 0, 0]))
#                 img_name = str(img_name)
#                 img_name = img_name.split("\\")[len(img_name.split("\\")) - 1]
#                 img_name = img_name.split(".")[0] + ".jpg"
#                 cv2.imwrite(os.path.join(path_, sub_save_path, img_name), img)
