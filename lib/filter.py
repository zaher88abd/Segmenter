import lib.plant_features as pf
import lib.augment_data as ad
import cv2
import numpy as np


# sys.path.insert(0, '/home/hallab/bonnet/train_py/dataset/aux_scripts')


# mask_name = "/media/hallab/a2d8ba2d-2b9a-457e-9344-0c65c5e866c0/hallab/Downloads/ijrr_annotations_160523
# /bonirob_2016-05-23-10-37-10_0_frame27_GroundTruth_color.png"
# file_name = "/home/hallab/Downloads/bonirob_2016-05-23-10-37-10_0/camera/jai/rgb/rgb_00027.png"
# NIR_name = "/home/hallab/Downloads/bonirob_2016-05-23-10-37-10_0/camera/jai/nir/nir_00027.png"


def normalize(rgb_image, nir_image):
    B, G, R = cv2.split(rgb_image)

    B = np.array(B.astype(float))
    G = np.array(G.astype(float))
    R = np.array(R.astype(float))

    B_ = np.zeros((B.shape[0], B.shape[1]))
    G_ = np.zeros((G.shape[0], G.shape[1]))
    R_ = np.zeros((R.shape[0], R.shape[1]))
    intensity = np.zeros((R.shape[0], R.shape[1]))

    # [height][width]
    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            intensity[i][j] = B[i][j] + G[i][j] + R[i][j]

            B_[i][j] = float(B[i][j]) / float(intensity[i][j])
            G_[i][j] = float(G[i][j]) / float(intensity[i][j])
            R_[i][j] = float(R[i][j]) / float(intensity[i][j])

    normalized_rgb = cv2.merge((B_, G_, R_))
    normalized_nir = nir_image.astype(float) / 255.0

    return normalized_rgb, normalized_nir


def NDVI(rgb, nir):
    B, G, R = cv2.split(rgb)

    ndvi = np.divide((nir - R), (nir + R))

    return ndvi


def scale_image(im):
    scaled = ((im - (-1)) / (1 - (-1))) * (255.0 - 0)

    return scaled


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
        exgr = None
        exgr_mask = None
        exgr = pf.exgreen(rgb_img)
        print("Exgr shape: ", exgr.shape)
        # util.im_gray_plt(exgr, "exgreen ")
        # cv2.imshow("exgr", exgr)
        exgr_mask = pf.thresh(exgr, 0)
        # util.im_gray_plt(exgr_mask, "exgreen mask")
        # cv2.imshow("exgr_mask", exgr_mask)

        c = pf.cive(rgb_img)
        print("cive shape: ", c.shape)
        # cv2.imshow("cive", c)
        c_mask = pf.thresh(c, 0)
        # cv2.imshow("cive_mask", c_mask)

        exr = pf.exred(rgb_img)
        print("Exred shape: ", exr.shape)
        # cv2.imshow("exr", exr)
        exr_mask = pf.thresh(exr, 0)
        # cv2.imshow("exr_mask", exr_mask)
        return exgr_mask

    # get NDI
    if filter_num == 2:
        ndi = pf.ndi(rgb_img)
        print("NDI shape: ", ndi.shape)
        # cv2.imshow("ndi", ndi)
        ndi_mask = pf.thresh(ndi, 0)
        # cv2.imshow("ndi_mask", exr_mask)

        # get hsv
        h = pf.hsv(rgb_img)
        # cv2.imshow("h", h)
        h_mask = pf.thresh(h[:, :, 0], 0)
        # cv2.imshow("h_mask", h_mask)

        exgr = pf.exgreen(rgb_img)
        g = pf.gradients(exgr, 'x')
        print("Gradient x shape: ", g.shape)
        # y gradient
        # cv2.imshow("gradient_x", g)

        g = pf.gradients(exgr, 'y')
        print("Gradient y shape: ", g.shape)
        # cv2.imshow("gradient_y", g)

        exgr = pf.exgreen(rgb_img)
        lplc = pf.laplacian(exgr)
        # cv2.imshow("lplc", lplc)

        exgr = pf.exgreen(rgb_img)
        e = pf.edges(exgr)
        print("Edge shape: ", e.shape)
        # cv2.imshow("edges", e)

        exgr = pf.exgreen(rgb_img)
        exgr_mask = pf.thresh(exgr, 0)
        w = pf.watershed(rgb_img, exgr, exgr_mask)
        # cv2.imshow("watershed_", w)

        exgr = pf.exgreen(rgb_img)
        exgr_mask = pf.thresh(exgr, 0)
        m = pf.mask_multidim(rgb_img, exgr_mask)
        # cv2.imshow("m", m)
        return m

        mgray = pf.mask_multidim(exgr, exgr_mask)
        # print("mgray shape: ", mgray.shape)
        # cv2.imshow("mgray", mgray)

        n = pf.chanelwise_norm(rgb_img)
        print("n shape: ", n.shape)
        # cv2.imshow("normalized", n)

    # proper_h = 384
    # proper_w = 512
    # # resize to see how it works with kernels
    # rgb_img = ad.resize(rgb_img, [proper_h, proper_w])
    # NIR_img = ad.resize(NIR_img, [proper_h, proper_w])

    # normalized_rgb, normalized_nir = normalize(rgb_img, NIR_img)

    # ndvi_image = NDVI(normalized_rgb, normalized_nir)
    # ndvi_image = scale_image(ndvi_image)
    # ndvi_image = ndvi_image.astype(np.uint8)
    #
    # ndvi_image_mask = pf.thresh(ndvi_image, 0)
