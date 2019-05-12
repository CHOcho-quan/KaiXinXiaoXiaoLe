import cv2
import numpy as np

def preprocessing(image, lightness, var):
    """
    Preprocessing the image if the image is too light or less contrary
    image : input image to be changed
    lightness : the lightness of the given image
    var : the given varience of the given image

    """
    if (lightness < 95):
        gamma = 1 / 2.2
        little = image.astype(np.float32) / 255
        corrected1 = np.power(little, gamma)
        corrected1 = (corrected1 * 255).astype(np.uint8)
        print("...Correcting Lightness...")
    else:
        corrected1 = image

    if var > 150:
        hsv2 = cv2.cvtColor(corrected1, cv2.COLOR_RGB2HSV)
        corrected2 = cv2.equalizeHist(hsv2[:, :, 2])
        corrected2 = cv2.cvtColor(corrected2, cv2.COLOR_HSV2RGB)
        print ("...Correcting Contrast...")
    else:
        corrected2 = corrected1

    return corrected2

def findSingle(image):
    """
    Given the image find the single length of a box of the animals
    image : the given image sliced only having the mact of the animals

    """
    maxNum = 9
    return int(image.shape[0] / maxNum)
