import utils
import cv2
import numpy as np

if __name__ == '__main__':
    # Image Preprocessing
    img = cv2.imread('kxxxl2.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lightness = np.mean(hsv[:, :, 2])
    var = np.std(hsv[:, :, 2])
    corrected = utils.preprocessing(img, lightness, var)

    # The First step is to locate the screen of my Pad

    # Getting the screen, now we are going to get the animals as a matrix
    # Cut the mask to get the animal matrix
    mask = cv2.inRange(hsv, np.array([100, 60, 60]), np.array([124, 255, 255]))
    y, x = mask.shape
    mask = mask[int(y / 5):int(y * 5.05 / 6), :]
    img = img[int(y / 5):int(y * 5.05 / 6), :]

    # Using Open operation to make the noise free of the image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Now try to count how many animals are there in the matrix
    indexes = np.array(np.argwhere(mask))
    top = np.min(indexes[:, 0])
    bottom = np.max(indexes[:, 0])
    left = np.min(indexes[:, 1])
    right = np.max(indexes[:, 1])
    # singleLength = utils.findSingle(image=mask)
    # animalHorizontal = min(int((right - left) / singleLength) + 1, 9)
    # animalVertical = min(int((bottom - top) / singleLength) + 1, 9)
    animalVertical = 7
    animalHorizontal = 7
    singleLength = int((right - left) / animalVertical)
    print(animalVertical, animalHorizontal)

    # Now we construct the total animal matrix up to single animals
    animals = np.zeros(shape=(animalVertical, animalHorizontal))
    originalMatrix = img[top:bottom, left:right]
    HSVMatrix = cv2.cvtColor(originalMatrix, cv2.COLOR_BGR2HSV)

    for y in range(animalVertical):
        for x in range(animalHorizontal):
            animals[y, x] = np.mean(HSVMatrix[y*singleLength:(y+1)*singleLength, x*singleLength:(x+1)*singleLength, 0])
    print(animals)
    cv2.imshow("originalMatrix", originalMatrix)
    cv2.waitKey(0)
