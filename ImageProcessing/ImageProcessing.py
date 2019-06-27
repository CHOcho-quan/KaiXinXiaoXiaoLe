import utils
import cv2
import numpy as np

def getPadLoc(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lightness = np.mean(hsv[:, :, 2])
    var = np.std(hsv[:, :, 2])
    corrected = utils.preprocessing(img, lightness, var)
    hsv = cv2.cvtColor(corrected, cv2.COLOR_BGR2HSV)

    _, binary = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10, 10))
    binary2 = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("bianry", binary2)
    # cv2.waitKey(0)
    pixelList = np.where(binary2==255)
    left = np.min(pixelList[1])
    right = np.max(pixelList[1])
    top = np.min(pixelList[0])
    bottom = np.max(pixelList[0])

    img = img[top:bottom, left:right]
    hsv = hsv[top:bottom, left:right]

    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    return img, hsv, (top, bottom, left, right)

def getXXLLoc(img, hsv):
    y, x, _ = img.shape
    img = img[int(y * 1.1 / 4):int(y * 5 / 6), int(x / 7):int(x * 5.1 / 6)]
    hsv = hsv[int(y * 1.1 / 4):int(y * 5 / 6), int(x / 7):int(x * 5.1 / 6)]
    mask = cv2.inRange(hsv, np.array([90, 0, 0]), np.array([124, 255, 255]))
    mask2 = cv2.inRange(hsv, np.array([0, 0, 185]), np.array([180, 55, 255]))

    # try_mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 100]))
    #
    # cv2.imshow("t", img)
    # cv2.waitKey(0)

    mask = cv2.bitwise_or(mask, mask2)

    # cv2.imshow("t", img)
    # cv2.waitKey(0)
    #
    # cv2.imshow("t", mask)
    # cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15, 15))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(10, 10))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # cv2.imshow("Try", mask)
    # cv2.waitKey(0)

    VerticalHist = np.sum(255-mask, axis=0)
    HorizontalHist = np.sum(255-mask, axis=1)
    print(VerticalHist / 255, mask.shape[1])
    indexes = np.argwhere(VerticalHist / 255 > mask.shape[1] / 4)
    indexes2 = np.argwhere(HorizontalHist / 255 > mask.shape[0] / 5)
    pixelList = np.where(mask==0)

    left = max(np.min(indexes)-10, 0)
    right = np.max(indexes)+10
    top = max(np.min(indexes2)-10, 0)
    bottom = np.max(indexes2)+10
    print(left, right, top, bottom)

    img2 = img[top:bottom, left:right]
    hsv2 = hsv[top:bottom, left:right]

    # cv2.imshow("Try", img2)
    # cv2.waitKey(0)

    return img, img2, hsv2, int(y * 1.1 / 4), top, bottom, int(x / 7), left, right

def getRowColumnNum(img, img2, right, left, bottom, top):
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    singleLength = utils.findSingle(img)
    animalHorizontal = min(int((right - left) / singleLength) + 1, 9)
    animalVertical = min(int((bottom - top) / singleLength) + 1, 9)
    print(animalVertical, animalHorizontal)
    if img2.shape[0] / singleLength < animalVertical - 0.5:
        animalVertical -= 1
    if img2.shape[1] / singleLength < animalHorizontal - 0.5:
        animalHorizontal -= 1
    print(animalVertical, animalHorizontal)
    return animalVertical, animalHorizontal, singleLength

def getAnimalMatrix(singleLength, animalVertical, animalHorizontal, img2):
    animals = np.zeros(shape=(animalVertical, animalHorizontal))
    originalMatrix = img2
    HSVMatrix = cv2.cvtColor(originalMatrix, cv2.COLOR_BGR2HSV)
    offset = 5

    for y in range(animalVertical):
        for x in range(animalHorizontal):
            b = np.mean(originalMatrix[y*singleLength:(y+1)*singleLength, x*singleLength:(x+1)*singleLength, 0])
            g = np.mean(originalMatrix[y*singleLength:(y+1)*singleLength, x*singleLength:(x+1)*singleLength, 1])
            r = np.mean(originalMatrix[y*singleLength:(y+1)*singleLength, x*singleLength:(x+1)*singleLength, 2])
            print(b, g, r)
            # if b > 150:
            #     animals[y, x] = 0
            #     continue
            if g > b and g > r:
                animals[y, x] = 3
            if r > g and r > b:
                if b > g:
                    if b > 100 and g > 100:
                        animals[y, x] = 7
                    elif b > 100:
                        animals[y, x] = 6
                    else:
                        animals[y, x] = 1
                else:
                    if g - b > 15:
                        animals[y, x] = 2
                    else:
                        animals[y, x] = 4
            if b > r and b > g:
                if r > g:
                    animals[y, x] = 6
                if g > r:
                    # 0 or 4
                    if b > 150:
                        animals[y, x] = 0
                    else:
                        animals[y, x] = 5
    return animals

if __name__ == '__main__':
    # Image Preprocessing

    camera = cv2.VideoCapture(0)
    success, ori_img = camera.read()
    img, hsv, (top, bottom, left, right) = getPadLoc(ori_img)
    img3, img2, hsv2, biasy, top2, bottom2, biasx, left2, right2 = getXXLLoc(img, hsv)
    animalVertical, animalHorizontal, singleLength = getRowColumnNum(img3, img2, right2, left2, bottom2, top2)
    while (success):
        img2 = ori_img[(biasy+top+top2):(biasy+top+bottom2), (biasx+left+left2):(biasx+left+right2)]
        mask2 = cv2.inRange(cv2.cvtColor(img2, cv2.COLOR_BGR2HSV), np.array([0, 0, 185]), np.array([180, 55, 255]))
        cv2.imshow("mask2", mask2)
        cv2.waitKey(0)
        if np.count_nonzero(mask2) / mask2.shape[0]*mask2.shape[1] > 0.6:
            print("WIN")
        # img2 = ori_img[top:bottom, left:right]
        # img2 = img2[top2:bottom2, left2:right2]
        cv2.imshow('img2', img2)
        cv2.waitKey(0)

        # Now we construct the total animal matrix up to single animals
        animals = getAnimalMatrix(singleLength, animalVertical, animalHorizontal, img2)

        """
        0 : Blank, 1 : Fox, 2 : Chicken, 3 : Frog, 4 : Bear, 5 : Blueshit, 6 : Hawk, 7 : Phinex

        """
        print(animals)

        success, ori_img = camera.read()
