import cv2


def get_image_dimensions(image_fp):
    """
    Returns the dimensions of the image
    :param image_fp:
    :return: width, height
    """
    w = cv2.imread(image_fp).shape[0]
    h = cv2.imread(image_fp).shape[1]
    return w, h
