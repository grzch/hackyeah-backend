import numpy as np

import cv2

def path_to_img(path):
    bgr_img = cv2.imread(path)
    return cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

def bytes_to_img(img_bytes):
    img_array = np.asarray(bytearray(img_bytes), dtype=np.uint8)
    bgr_img = cv2.imdecode(img_array, -1)
    return cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
