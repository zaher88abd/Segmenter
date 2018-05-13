import lib.plant_features as pf
import lib.augment_data as ad
import numpy as np
import cv2

BLUE = np.array([255, 0, 0])


def filter_image(original_img, filter_num):
    rgb_img = original_img  # cv2.imread(original_img, cv2.IMREAD_UNCHANGED)

    proper_h = 512
    proper_w = 640
    # resize to see how it works with kernels
    rgb_img = ad.resize(rgb_img, [proper_h, proper_w])
    if filter_num == 0:
        return rgb_img
    if rgb_img is None:
        print("Rgb image doesn't exist")
        quit()

    # EXGR
    if filter_num == 1:
        exgr = pf.exgreen(rgb_img)
        exgr_mask = pf.thresh(exgr, 0)
        return exgr_mask

    # mask_multidim
    if filter_num == 2:
        exgr = pf.exgreen(rgb_img)
        exgr_mask = pf.thresh(exgr, 0)
        return pf.mask_multidim(rgb_img, exgr_mask)

    # Cive
    if filter_num == 3:
        return pf.cive(rgb_img)

    # Exred
    if filter_num == 4:
        return pf.exred(rgb_img)

    # ndi
    if filter_num == 5:
        hsv = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)

        lower_black = np.array([36, 100, 70], dtype="uint8")
        upper_black = np.array([70, 255, 175], dtype="uint8")
        mask = cv2.inRange(hsv, lower_black, upper_black)

        img = np.zeros((mask.shape[0], mask.shape[1], 3))
        img[np.where(mask == 255)] = BLUE
        img = img.astype(np.uint8)
        return img

        # Hsv
    if filter_num == 6:
        ss = pf.hsv(rgb_img)
        print("hsv", np.shape(ss))
        return ss

    # edges
    if filter_num == 7:
        return pf.edges(rgb_img)

    # laplacian
    if filter_num == 8:
        return pf.laplacian(rgb_img)
