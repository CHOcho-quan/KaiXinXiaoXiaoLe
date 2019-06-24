import utils
import cv2
import numpy as np

if __name__ == '__main__':
    # Image Preprocessing
    img = cv2.imread('kxxxl3.png')

    camera = cv2.VideoCapture(0)
    success, img = camera.read()
    while (success):
        # The First step is to locate the screen of my Pad
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

        y, x, _ = img.shape
        img = img[int(y / 4.5):int(y * 5.3 / 6), int(x / 7):int(x * 5 / 6)]
        hsv = hsv[int(y / 4.5):int(y * 5.3 / 6), int(x / 7):int(x * 5 / 6)]
        mask = cv2.inRange(hsv, np.array([90, 0, 0]), np.array([124, 255, 255]))

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(35, 35))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(10, 10))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

        cv2.imshow("Try", mask[:, ::-1])
        cv2.waitKey(0)

        VerticalHist = np.sum(255-mask, axis=0)
        HorizontalHist = np.sum(255-mask, axis=1)
        print(VerticalHist / 255, mask.shape[1])
        indexes = np.argwhere(VerticalHist / 255 > mask.shape[1] / 6)
        indexes2 = np.argwhere(HorizontalHist / 255 > mask.shape[0] / 7)
        pixelList = np.where(mask==0)

        left = max(np.min(indexes)-10, 0)
        right = np.max(indexes)+10
        top = max(np.min(indexes2)-5, 0)
        bottom = np.max(indexes2)+5
        print(left, right, top, bottom)

        img2 = img[top:bottom, left:right]
        hsv2 = hsv[top:bottom, left:right]
        # cv2.imshow("Try", mask[top:bottom, left:right])
        # cv2.waitKey(0)

        singleLength = utils.findSingle(img)
        animalHorizontal = min(int((right - left) / singleLength) + 1, 9)
        animalVertical = min(int((bottom - top) / singleLength) + 1, 9)
        if img2.shape[0] / singleLength < animalVertical - 0.5:
            animalVertical -= 1
        if img2.shape[1] / singleLength < animalHorizontal - 0.5:
            animalHorizontal -= 1
        print(animalVertical, animalHorizontal)

        # Now we construct the total animal matrix up to single animals
        animals = np.zeros(shape=(animalVertical, animalHorizontal))
        originalMatrix = img[top:bottom, left:right]
        HSVMatrix = cv2.cvtColor(originalMatrix, cv2.COLOR_BGR2HSV)
        offset = 5

        cv2.imshow("Try", img2)
        cv2.waitKey(0)

        """
        0 : Blank, 1 : Fox, 2 : Frog, 3 : Chicken, 4 : BlueShit, 5 : hawk, 6 : Bear, 7 : Phinex

        """
        for y in range(animalVertical):
            for x in range(animalHorizontal):
                b = np.mean(originalMatrix[y*singleLength:(y+1)*singleLength, x*singleLength:(x+1)*singleLength, 0])
                g = np.mean(originalMatrix[y*singleLength:(y+1)*singleLength, x*singleLength:(x+1)*singleLength, 1])
                r = np.mean(originalMatrix[y*singleLength:(y+1)*singleLength, x*singleLength:(x+1)*singleLength, 2])
                # print(b, g, r)
                if g > b and g > r:
                    animals[y, x] = 2
                if r > g and r > b:
                    if b > g:
                        animals[y, x] = 1
                    else:
                        if g > 2 * b:
                            animals[y, x] = 3
                        animals[y, x] = 6
                if b > r and b > g:
                    if r > g:
                        animals[y, x] = 5
                    if g > r:
                        # 0 or 4
                        if b > 110:
                            animals[y, x] = 0
                        else:
                            animals[y, x] = 4
                # print(np.mean(HSVMatrix[y*singleLength:(y+1)*singleLength, x*singleLength:(x+1)*singleLength, 0]))
                # cv2.imshow("hsv", originalMatrix[y*singleLength:(y+1)*singleLength, x*singleLength+offset:(x+1)*singleLength+offset, :])
                # cv2.waitKey(0)
        print(animals)

        success, img = camera.read()
