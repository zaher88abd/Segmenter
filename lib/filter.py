import lib.plant_features as pf
import lib.augment_data as ad


def filter_image(original_img, filter_num):
    if filter_num == 0:
        return original_img
    rgb_img = original_img  # cv2.imread(original_img, cv2.IMREAD_UNCHANGED)

    proper_h = 384
    proper_w = 512
    # resize to see how it works with kernels
    rgb_img = ad.resize(rgb_img, [proper_h, proper_w])
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
        return pf.ndi(rgb_img)

    # Hsv
    if filter_num == 6:
        return pf.hsv(rgb_img)

    # edges
    if filter_num == 7:
        return pf.edges(rgb_img)

    # laplacian
    if filter_num == 8:
        return pf.laplacian(rgb_img)


