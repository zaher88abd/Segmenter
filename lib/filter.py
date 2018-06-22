import lib.plant_features as pf
import lib.augment_data as ad
import numpy as np
import cv2

BLUE = np.array([255, 0, 0])
WHITE = np.array([255, 255, 255])


def filter_image(original_img, filter_num, self):
    rgb_img = original_img  # cv2.imread(original_img, cv2.IMREAD_UNCHANGED)

    proper_h = 512
    proper_w = 640
    # resize to see how it works with kernels
    rgb_img = ad.resize(rgb_img, [proper_h, proper_w])

    if filter_num == 0:
        if len(self.custom_hsv_filters) > 0:
            return custom_hsv_img(rgb_img, self)
        return rgb_img
    if rgb_img is None:
        print("Rgb image doesn't exist")
        quit()

    # EXGR
    if filter_num == 1:
        exgr = pf.exgreen(rgb_img)
        exgr_mask = pf.thresh(exgr, int(self.exgr_slider.value()), 0)
        return exgr_mask

    # mask_multidim
    if filter_num == 2:
        exgr = pf.exgreen(rgb_img)
        exgr_mask = pf.thresh(exgr, int(self.exgr_slider.value()), 0)
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
        img[np.where(mask == 255)] = WHITE
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

    # custom
    if filter_num == 9:
        hsv = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
        saved_mask = pre_filter_with_hsv_filters(hsv, self.custom_hsv_filters)
        lower_black = np.array([self.hue_min_slider.value(), self.saturation_min_slider.value(), self.value_min_slider.value()], dtype="uint8")
        upper_black = np.array([self.hue_max_slider.value(), self.saturation_max_slider.value(), self.value_max_slider.value()], dtype="uint8")
        slider_mask = cv2.inRange(hsv, lower_black, upper_black)
        if saved_mask is not None:
            mask = cv2.bitwise_or(saved_mask, slider_mask)
        else:
            mask = slider_mask

        img = np.zeros((mask.shape[0], mask.shape[1], 3))
        img[np.where(mask == 255)] = WHITE
        img = img.astype(np.uint8)
        return img


def pre_filter_with_hsv_filters(hsv, filters):
    final_mask = None
    for filter in filters:
        lower_black = np.array([filter[0][0], filter[1][0], filter[2][0]], dtype="uint8")
        upper_black = np.array([filter[0][1], filter[1][1], filter[2][1]], dtype="uint8")
        mask = cv2.inRange(hsv, lower_black, upper_black)
        if final_mask is not None:
            final_mask = cv2.bitwise_or(final_mask, mask)
        else:
            final_mask = mask
    return final_mask


def custom_hsv_img(image, self):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saved_mask = pre_filter_with_hsv_filters(hsv, self.custom_hsv_filters)
    if saved_mask is not None:
        mask = saved_mask
    else:
        mask = hsv

    img = np.zeros((mask.shape[0], mask.shape[1], 3))
    img[np.where(mask == 255)] = WHITE
    img = img.astype(np.uint8)
    return img